from dotenv import load_dotenv
from flask import Flask, render_template
from threading import Thread
import os
import socket
from queue import Queue

load_dotenv()
ip_address = os.getenv('IP_ADDRESS')
web_port = int(os.getenv('WEB_PORT'))
socket_port = int(os.getenv('SOCKET_PORT'))

# I've tried over 8 hours debugging this
# The client_sockets queue just can't work across threads
# Flask has to run on the main thread
# Socket has to be a separate thread
# I've tried using a global variable, but it doesn't work
# The send_command does not see the updated client_sockets value no matter what

class Server:
    def __init__(self):
        self.client_sockets = Queue()

        print("Creating socket...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Setting socket options...")
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Binding to port {socket_port}...")
        try:
            self.s.bind((ip_address, socket_port))
            print("Successfully bound to port.")
        except Exception as e:
            print(f"Failed to bind to port. Error: {e}")

        print("Putting socket into listening mode...")
        try:
            self.s.listen(1)
            print("Socket is now listening.")
        except Exception as e:
            print(f"Failed to put socket into listening mode. Error: {e}")

    def handle_client(self):
        while True:
            client_socket, addr = self.s.accept()

            self.client_sockets.put(client_socket)
            print(f"DEBUG: handle_client() - Client connected from: {addr}. Total clients: {self.client_sockets.qsize()}")
            print(f"DEBUG: handle_client() - All clients: {self.client_sockets}")

    def send_command(self, message):
        try:
            print(f"DEBUG: send_command() - Sending to all clients: {message}")
            print(f"DEBUG: send_command() - Total clients: {self.client_sockets.qsize()}")
            print(f"DEBUG: send_command() - All clients: {self.client_sockets}")

            # Create a temporary queue to hold the client sockets
            temp_queue = Queue()

            # Iterate over the queue to send messages
            while not self.client_sockets.empty():
                client_socket = self.client_sockets.get()
                client_socket.send(message.encode())
                print(f"Sent to client: {message}")

                # Add the client socket back to the temporary queue
                temp_queue.put(client_socket)

            # Replace the original queue with the temporary queue
            self.client_sockets = temp_queue
        except Exception as e:
            print(f"An error occurred while sending to all clients. Error: {e}")

    def run(self):
        # Run the socket server in a separate thread
        Thread(target=self.handle_client).start()

server = Server()
        
# ========================================================================================================
# FLASK SERVER
# ========================================================================================================

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trigger_enable_system')
def trigger_enable_system():
    print("Home Security System ENABLED.")
    server.send_command(b'ENABLE_SYSTEM')
    return '200 OK'

@app.route('/trigger_disable_system')
def trigger_disable_system():
    print("Home Security System DISABLED.")
    server.send_command(b'DISABLE_SYSTEM')
    return '200 OK'

@app.route('/trigger_enable_lightRoom')
def trigger_enable_lightRoom():
    print("Room Light ENABLED.")
    server.send_command(b'ENABLE_LIGHT_ROOM')
    return '200 OK'

@app.route('/trigger_disable_lightRoom')
def trigger_disable_lightRoom():
    print("Room Light DISABLED.")
    server.send_command(b'DISABLE_LIGHT_ROOM')
    return '200 OK'

@app.route('/trigger_enable_fanRoom')
def trigger_enable_fanRoom():
    print("Room Fan ENABLED.")
    server.send_command(b'ENABLE_FAN_ROOM')
    return '200 OK'

@app.route('/trigger_disable_fanRoom')
def trigger_disable_fanRoom():
    print("Room Fan DISABLED.")
    server.send_command(b'DISABLE_FAN_ROOM')
    return '200 OK'

@app.route('/trigger_enable_alarm')
def trigger_enable_alarm():
    print("Alarm ENABLED.")
    server.send_command(b'ENABLE_ALARM')
    return '200 OK'

@app.route('/trigger_disable_alarm')
def trigger_disable_alarm():
    print("Alarm DISABLED.")
    server.send_command(b'DISABLE_ALARM')
    return '200 OK'

@app.route('/trigger_enable_light')
def trigger_enable_light():
    print("Light ENABLED.")
    server.send_command(b'ENABLE_LIGHT')
    return '200 OK'

@app.route('/trigger_disable_light')
def trigger_disable_light():
    print("Light DISABLED.")
    server.send_command(b'DISABLE_LIGHT')
    return '200 OK'

@app.route('/trigger_enable_fan')
def trigger_enable_fan():
    print("Fan ENABLED.")
    server.send_command(b'ENABLE_LIGHT')
    return '200 OK'

@app.route('/trigger_disable_fan')
def trigger_disable_fan():
    print("Fan DISABLED.")
    server.send_command(b'DISABLE_LIGHT')
    return '200 OK'


# ========================================================================================================
# MAIN
# ========================================================================================================
def main():
    server.run()
    
    # Run the Flask app in the main thread
    app.run(debug=True, host=ip_address, port=web_port)
    
if __name__ == '__main__':
    main()