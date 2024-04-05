#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import logging
import socketserver
from http import server
from threading import Condition, Thread, Event
import signal
import sys
import time
import requests
import os 
from datetime import  datetime
from dotenv import load_dotenv

import socketio

from gpiozero import DistanceSensor

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

masterActive = True

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with camera_stream.output.condition:
                        camera_stream.output.condition.wait()
                        frame = camera_stream.output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class CameraStream:
    def __init__(self):
        self.output = StreamingOutput()
        self.picam2 = Picamera2()
        self.server = None
        self.thread = None
        self.ultrasonic = DistanceSensor(echo = 17, trigger =4)
        self.exit_event = Event()
        self.livefeed_active = False

    def start_streaming(self):
        if not self.server and masterActive == True:
            self.livefeed_active = True
            self.picam2.configure(self.picam2.create_video_configuration(main={"size": (640, 480)}))
            self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
            StreamingHandler.output = self.output
            self.server = StreamingServer(('', 8000), StreamingHandler)
            self.thread = Thread(target=self.server.serve_forever)
            self.thread.start()
            print("Streaming started...")

    def stop_streaming(self):
        if self.server: 
            self.livefeed_active = False
            self.picam2.stop_recording()
            self.server.shutdown()
            self.server.server_close()
            self.thread.join()
            self.server = None
            print("Streaming stopped...")

        # Function to take a photo and save it locally with a unique timestamp in the filename
    def take_photo(self,base_path):
        os.makedirs(base_path, exist_ok=True)
        # Generate a unique filename with a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(base_path, f"photo_{timestamp}.jpg")
        # Configure and capture
        self.picam2.start_and_capture_file(file_path, show_preview=False)
        return file_path

    # Function to send the photo to the webserver
    def send_photo(self,file_path):
        url = 'http://192.168.0.186:5000/upload'  # Change WEB_SERVER_IP to your webserver's IP and ensure the endpoint matches
        with open(file_path, 'rb') as f:
            files = {'photo': (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
        print(response.text)
        # Optionally, remove the local file after upload
        os.remove(file_path)

    def monitor_distance_trigger(self):
        liveFeedMessagePrinted = False
        lastDistance = None
        while not self.exit_event.is_set():
            # Active checking loop
            currentDistance = self.ultrasonic.distance
            if not masterActive:
                time.sleep(1)
                continue

            if currentDistance < 0.06:
                if self.livefeed_active:
                    self.stop_streaming()
                    print("Object in range, taking photo")
                    file_path=self.take_photo('./photo')
                    self.send_photo(file_path)
                    sio.emit('intruder_detected',{'message':'Intruder Detected!'})
                    self.start_streaming()
                else:
                    print("Object in range, taking photo")
                    file_path=self.take_photo('./photo')
                    self.send_photo(file_path)
                    sio.emit('intruder_detected',{'message':'Intruder Detected!'})

        print("Monitor thread exiting")


camera_stream = CameraStream()
sio = socketio.Client()

@sio.event 
def connect():
    print('Connected to the server')
    sio.emit('join_securitypi_room', {})

@sio.event
def start_live_feed(data):
    if data.get('command') == 'start':
        camera_stream.start_streaming()

@sio.event
def stop_live_feed(data):
    if data.get('command') == 'stop':
        camera_stream.stop_streaming()

@sio.event
def message(data):
    print(data)
    global masterActive
    if data == "all on":
        masterActive = True
        camera_stream.start_streaming()
    elif data == "all off":
        masterActive = False

def signal_handler(sig, frame):
    print('Signal caught, stopping streaming...')
    camera_stream.stop_streaming()
    sys.exit(0)



signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# Start streaming automatically
#camera_stream.start_streaming()
def main():
    load_dotenv()
    ip_address = os.getenv('IP_ADDRESS')
    port = int(os.getenv('PORT'))
    print(f"Attempting to connect to {ip_address}:{port}...")

    monitor_thread = Thread(target=camera_stream.monitor_distance_trigger)
    monitor_thread.start()
    try:
        sio.connect(f'http://{ip_address}:{port}')
        print("Successfully connected to the server.")
        camera_stream.start_streaming()

        while True:
            pass
            # Ask the user what they want to do
            #action = input("Enter 1 to start streaming, 2 to stop streaming, or 0 to exit: ")
            
            #if action == '1':
             #   camera_stream.start_streaming()
            #elif action == '2':
             #   camera_stream.stop_streaming()
            #elif action == '0':
             #   print("Exiting...")
              #  camera_stream.stop_streaming()  # Ensure streaming is stopped before exiting
              #  break  # Exit the loop, leading to the cleanup in the finally block
            #else:
             #   print("Invalid input. Please enter 1, 2, or 0.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # This finally block now correctly handles cleanup when exiting the loop
        camera_stream.exit_event.set()
        monitor_thread.join()
        print("Program exited")
        sio.disconnect()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()