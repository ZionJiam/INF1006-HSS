from flask import Flask, render_template, Response
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to trigger Python code for the ENTIRE SYSTEM
@app.route('/trigger_enable_system')
def trigger_enable_system():
    # Python code to print something
    print("Home Security System ENABLED. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_disable_system')
def trigger_disable_system():
    # Python code to print something
    print("Home Security System DISABLED. Python code executed.")
    return 'Python code executed successfully'



# Route to trigger Python code for light module FOR ROOM
@app.route('/trigger_enable_lightRoom')
def trigger_enable_lightRoom():
    # Python code to print something
    print("Room Light ENABLED. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_disable_lightRoom')
def trigger_disable_lightRoom():
    # Python code to print something
    print("Room Light DISABLED. Python code executed.")
    return 'Python code executed successfully'

# Route to trigger Python code for fan module FOR ROOM
@app.route('/trigger_enable_fanRoom')
def trigger_enable_fanRoom():
    # Python code to print something
    print("Room Fan ENABLED. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_disable_fanRoom')
def trigger_disable_fanRoom():
    # Python code to print something
    print("Room Fan DISABLED. Python code executed.")
    return 'Python code executed successfully'




# Route to trigger Python code for alarm module
@app.route('/trigger_enable_alarm')
def trigger_enable_alarm():
    # Python code to print something
    print("Alarm ENABLED. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_disable_alarm')
def trigger_disable_alarm():
    # Python code to print something
    print("Alarm DISABLED. Python code executed.")
    return 'Python code executed successfully'

# Route to trigger Python code for light module
@app.route('/trigger_enable_light')
def trigger_enable_light():
    # Python code to print something
    print("light ENABLED. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_disable_light')
def trigger_disable_light():
    # Python code to print something
    print("light DISABLED. Python code executed.")
    return 'Python code executed successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)