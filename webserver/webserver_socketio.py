from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for,send_from_directory, Response
from flask_socketio import SocketIO, send, emit, join_room
from werkzeug.utils import secure_filename
import requests
import os

LATEST_IMAGES = []
load_dotenv()
ip_address = os.getenv('IP_ADDRESS')
web_port = int(os.getenv('WEB_PORT'))

app = Flask(__name__)
socketio = SocketIO(app)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'photo')

# ========================================================================================================
# SOCKET.IO
# ========================================================================================================

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    
@socketio.on('message')
def handle_message(message):
    emit('frontend', message, broadcast=True)
    print('Received message: ' + message)
    if message == 'light on':
        print("Turning on the light")
    elif message == 'light off':
        print("Turning off the light")
    elif message == 'fan on':
        print("Turning on the fan")
    elif message == 'fan off':
        print("Turning off the fan")
    elif message == 'all on':
        print("Turning on all devices")
    elif message == 'all off':
        print("Turning off all devices")
    else:
        print("Unknown command: " + message)

@socketio.on('intruder_detected')
def handle_intruder_detected(data):
    print("Intruder detected:", data['message'])
    socketio.emit('activate_alert',{'message':'Activate the buzzer and LEDs'})
        
def send_command(message):
    try:
        print(f"Sending to all clients: {message}")
        socketio.emit('message', message)
    except Exception as e:
        print(f"An error occurred while sending to all clients. Error: {e}")
        
        
# ========================================================================================================
# FLASK SERVER
# ========================================================================================================

@app.route('/')
def home():
    return render_template('index.html')

# All
@app.route('/trigger_enable_system')
def trigger_enable_system():
    print("Home Security System ENABLED.")
    send_command('all on')
    return '200 OK'

@app.route('/trigger_disable_system')
def trigger_disable_system():
    print("Home Security System DISABLED.")
    send_command('all off')
    return '200 OK'

# Room
@app.route('/trigger_enable_lightRoom')
def trigger_enable_lightRoom():
    print("Room Light ENABLED.")
    send_command('light on')
    return '200 OK'

@app.route('/trigger_disable_lightRoom')
def trigger_disable_lightRoom():
    print("Room Light DISABLED.")
    send_command('light off')
    return '200 OK'

@app.route('/trigger_enable_fanRoom')
def trigger_enable_fanRoom():
    print("Room Fan ENABLED.")
    send_command('fan on')
    return '200 OK'

@app.route('/trigger_disable_fanRoom')
def trigger_disable_fanRoom():
    print("Room Fan DISABLED.")
    send_command('fan off')
    return '200 OK'

# Alarm
@app.route('/trigger_enable_alarm')
def trigger_enable_alarm():
    print("Alarm ENABLED.")
    send_command('alarm on')
    return '200 OK'

@app.route('/trigger_disable_alarm')
def trigger_disable_alarm():
    print("Alarm DISABLED.")
    send_command('alarm off')
    return '200 OK'

@app.route('/trigger_enable_light')
def trigger_enable_light():
    print("Light ENABLED.")
    send_command('led on')
    return '200 OK'
@app.route('/trigger_disable_light')
def trigger_disable_light():
    print("light DISABLED.")
    send_command('led off')
    return '200 OK'


@app.route('/proxy_feed')
def proxy_feed():
    # URL of the live feed on the securitypi
    print('attempt')
    feed_url = 'http://raspberrypi.local:8000/stream.mjpg'

    # Make a request to the securitypi to get the feed
    resp = requests.get(feed_url, stream=True)

    # Stream the response back to the client
    return Response(resp.iter_content(chunk_size=10 * 1024),
                    content_type=resp.headers['Content-Type'])


@app.route('/upload', methods=['POST'])
def upload_file():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file = request.files['photo']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Update the list of the latest images (consider a thread-safe method if needed)
        LATEST_IMAGES.insert(0, filename)  # Insert the new image at the beginning of the list
        if len(LATEST_IMAGES) > 4:
            # Optionally remove the file of the oldest image
            os.remove(os.path.join(UPLOAD_FOLDER, LATEST_IMAGES[-1]))
            # Remove the oldest image from the list
            LATEST_IMAGES.pop()

        # Emit event with URLs for the latest images
        latest_image_urls = [url_for('uploaded_file', filename=f) for f in LATEST_IMAGES[:4]]
        socketio.emit('update_images', {'latest_images': latest_image_urls})
        print('Emitting update_images with:', [url_for('uploaded_file', filename=f) for f in LATEST_IMAGES[:4]])

        return 'File uploaded successfully', 200

@app.route('/photo/<filename>')
def uploaded_file(filename):
    return send_from_directory('photo', filename)

@app.route('/start_live_feed')
def start_live_feed():
    print("Starting live feed on securitypi.")
    # Your code to notify securitypi to start live feed
    socketio.emit('start_live_feed', {'command': 'start'}, room='securitypi_room')
    return '200 OK'

@app.route('/stop_live_feed')
def stop_live_feed():
    print("Stopping live feed on securitypi.")
    # Your code to notify securitypi to stop live feed
    socketio.emit('stop_live_feed', {'command': 'stop'}, room='securitypi_room')
    return '200 OK'

@socketio.on('join_securitypi_room')
def handle_join_securitypi_room(data):
    join_room('securitypi_room')
    print('Securitypi has joined the room.')
# ========================================================================================================
# MAIN
# ========================================================================================================

def main():
    socketio.run(app, debug=True, host=ip_address, port=web_port)

if __name__ == '__main__':
    main()