from dotenv import load_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import os

load_dotenv()
ip_address = os.getenv('IP_ADDRESS')
web_port = int(os.getenv('WEB_PORT'))

app = Flask(__name__)
socketio = SocketIO(app)

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
    send_command('alarm off')
    return '200 OK'

@app.route('/trigger_disable_alarm')
def trigger_disable_alarm():
    print("Alarm DISABLED.")
    send_command('alarm off')
    return '200 OK'


# ========================================================================================================
# MAIN
# ========================================================================================================

def main():
    socketio.run(app, debug=True, host=ip_address, port=web_port)

if __name__ == '__main__':
    main()