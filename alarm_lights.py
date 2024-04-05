#!/usr/bin/env python3
from dotenv import load_dotenv
import os

import RPi.GPIO as GPIO
import time
import socketio
import threading

light_on = False
alarm_on = False
count = 0

ALARM_PIN = 18
LIGHT_PIN = 19
lightActive = True
buzzerActive = True
frequency = 261
pwm = None

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.LOW)

    # Now that the GPIO mode is set, we can create the PWM instance
    global pwm
    pwm = GPIO.PWM(ALARM_PIN, frequency)

#  Function for blinking light
def light_on(duration, interval):
    while lightActive:
        end_time = time.time() + duration
        while time.time() < end_time and lightActive:  # Check lightActive in inner loop as well
            GPIO.output(LIGHT_PIN, GPIO.HIGH)
            time.sleep(interval)
            GPIO.output(LIGHT_PIN, GPIO.LOW)
            time.sleep(interval)

def alarm_on():
    pwm.start(50)  # Start the buzzer with a 50% duty cycle
    while buzzerActive:
        time.sleep(0.1)  # Small delay to prevent high CPU usage
    pwm.stop()  # Stop the buzzer when buzzerActive is set to False






# ========================================================================================================
# SOCKET.IO
# ========================================================================================================


sio = socketio.Client()

@sio.event
def connect():
    print("Successfully connected to the server.")

@sio.event
def disconnect():
    print("Disconnected from server.")

@sio.event
def message(data):
    print('Received from server: ' + data)
    global lightActive
    global buzzerActive
    if data == "all on":
        lightActive = True
        buzzerActive = True
    elif data == "all off":
        lightActive = False
        buzzerActive = False
    elif data == "led on":
        lightActive = True
    elif data == 'led off':
        lightActive = False
    elif data == 'alarm on':
        buzzerActive = True
    elif data == 'alarm off':
        buzzerActive = False



# Handler for 'activate_alert' event from the webserver
@sio.on('activate_alert')
def on_activate_alert(data):
    print(data['message'])
    # Create threads for alarm and light functions
    alarm_thread = threading.Thread(target=alarm_on)
    light_thread = threading.Thread(target=light_on, args=(5, 0.1))
    
    # Start the threads
    alarm_thread.start()
    light_thread.start()
        
# def handle_server_response(s):
#     while True:
#         # Receive the response from the server
#         response = s.recv(1024)
#         print('Received from server: ' + response)

#         if not handle_command(response):


        
# ========================================================================================================
# MAIN
# ========================================================================================================
        
def main():
    print("===== ALARM AND LIGHTS =====")
    print(f"Lights:\tpin {LIGHT_PIN}")
    print(f"Alarm:\tpin {ALARM_PIN}")
    load_dotenv()
    setupGPIO();

    ip_address = os.getenv('IP_ADDRESS')
    port = int(os.getenv('PORT'))
    try:
        print(f"Attempting to connect to {ip_address}:{port}...")
        sio.connect(f'http://{ip_address}:{port}')
        print("Successfully connected to the server.")

        while True:
            pass

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sio.disconnect()

if __name__ == "__main__":
    # Run the socket server in a separate thread

    # Run the main function in the main thread
    main()