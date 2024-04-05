#!/usr/bin/env python3
from dotenv import load_dotenv
import os

import RPi.GPIO as GPIO
import time
import socketio
import threading

light_on = False
fan_on = False
count = 0

LIGHT_PIN = 18
FAN_BUTTON_PIN = 23
FAN_PIN = 24
LIGHT_BUTTON_PIN = 25

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def switch(state=None, device='both'):
    global light_on, fan_on, count

    if device not in ['fan', 'light', 'both']:
        print("Invalid device. Please enter 'fan', 'light', or 'both'.")
        return

    if state is not None:
        if device == 'fan' or device == 'both':
            fan_on = state
        if device == 'light' or device == 'both':
            light_on = state
    else:
        if device == 'fan' or device == 'both':
            fan_on = not fan_on
        if device == 'light' or device == 'both':
            light_on = not light_on

    count += 1

    if light_on == True:
        print("Turning on Lights\tcount: " + str(count))
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
        sio.emit('message', 'light on')
    else:
        print("Turning off Lights\tcount: " + str(count))
        GPIO.output(LIGHT_PIN, GPIO.LOW)
        sio.emit('message', 'light off')

    if fan_on == True:
        print("Turning on Fan\tcount: " + str(count))
        GPIO.output(FAN_PIN, GPIO.HIGH)
        sio.emit('message', 'fan on')
    else:
        print("Turning off Fan\tcount: " + str(count))
        GPIO.output(FAN_PIN, GPIO.LOW)
        sio.emit('message', 'fan off')

def lightButtonPressCallback(channel):
    time.sleep(0.1)
    if GPIO.input(FAN_BUTTON_PIN) == GPIO.LOW:
        switch(device='fan')

def fanButtonPressCallback(channel):
    time.sleep(0.1)
    if GPIO.input(LIGHT_BUTTON_PIN) == GPIO.LOW:
        switch(device='light')

def detectButtonPress():
    GPIO.add_event_detect(FAN_BUTTON_PIN, GPIO.FALLING, callback=lightButtonPressCallback, bouncetime=300)
    GPIO.add_event_detect(LIGHT_BUTTON_PIN, GPIO.FALLING, callback=fanButtonPressCallback, bouncetime=300)
        
def handle_command(command):
    if command == "fan on":
        switch(True, 'fan')
    elif command == "fan off":
        switch(False, 'fan')
    elif command == "light on":
        switch(True, 'light')
    elif command == "light off":
        switch(False, 'light')
    elif command == "all on":
        switch(True, 'both')
    elif command == "all off":
        switch(False, 'both')
    elif command == "quit":
        return False
    else:
        print("Invalid command. Please enter 'fan on', 'fan off', 'light on', 'light off', 'all on', 'all off', or 'quit'.")
    return True


# ========================================================================================================
# SOCKET.IO
# ========================================================================================================

import socketio

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
    if not handle_command(data):
        sio.disconnect()
        
def handle_server_response(s):
    while True:
        # Receive the response from the server
        response = s.recv(1024)
        print('Received from server: ' + response)

        if not handle_command(response):
            break

def connect_webserver():
    load_dotenv()

    ip_address = os.getenv('IP_ADDRESS')
    port = int(os.getenv('PORT'))

    print(f"Attempting to connect to {ip_address}:{port}...")
    try:
        sio.connect(f'http://{ip_address}:{port}')
        print("Successfully connected to the server.")

        while True:
            command = input("Enter a command (fan on/fan off/light on/light off/all on/all off/quit): ").lower()

            sio.emit('message', command)

            if not handle_command(command):
                break

    except Exception as e:
        print(f"Failed to connect to the server. Error: {e}")
        print("Continuing without server connection...")
        
    sio.disconnect()

        
# ========================================================================================================
# MAIN
# ========================================================================================================
        
def main():
    print("===== FAN AND LIGHTS =====")
    print(f"Lights:\tpin {LIGHT_PIN}")
    print(f"Fan:\tpin {FAN_PIN}")
    print(f"Lights Button:\tpin {FAN_BUTTON_PIN}")
    print(f"Fan Button:\tpin {LIGHT_BUTTON_PIN}")

    setupGPIO()
    detectButtonPress()
    
if __name__ == "__main__":
    # Run the socket server in a separate thread
    threading.Thread(target=connect_webserver).start()

    # Run the main function in the main thread
    main()