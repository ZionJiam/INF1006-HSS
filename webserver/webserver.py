from flask import Flask, render_template, Response
from flask import Flask, render_template, Response
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to trigger Python code
@app.route('/trigger_python_code')
def trigger_python_code():
    # Python code to print something
    print("Toggle switch toggled ON. Python code executed.")
    return 'Python code executed successfully'

@app.route('/trigger_toggle_off')
def trigger_toggle_off():
    # Python code to print something
    print("Toggle switch toggled OFF. Python code executed.")
    return 'Python code executed successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)