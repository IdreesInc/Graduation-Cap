#!/usr/bin/env python
import time
import sys
import json
import socketio
import http.client as httplib

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageEnhance

print("Starting graduation cap!")

config = json.load(open("./config.json"))
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 100

display_brightness = config["brightness"] / 100
display_override = None

matrix = RGBMatrix(options = options)

sio = socketio.Client()

connected = False

def try_to_connect():
    if not connected:
        try:
            sio.connect(config["relayHost"])
        except Exception:
            print("Unable to connect to relay server")

def connected_to_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=0.5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

@sio.event
def connect():
    global connected
    connected = True
    print("Connection to relay server established!")
    sio.emit("graduation-cap-connected", "I'm in")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected from the relay server!")

@sio.event
def brightness(data):
    global display_brightness
    print('Message received, brightness -> ' + data)
    display_brightness = float(data) / 100

@sio.event
def display(data):
    global display_override
    print('Message received, display -> ' + data)
    display_override = int(data)

@sio.event
def relinquish(data):
    global display_override
    print('Message received, relinquish -> ' + data)
    display_override = None

def display_image(path):
    image = Image.open(path)
    image.thumbnail((matrix.width, matrix.height))
    enhancer = ImageEnhance.Brightness(image.convert('RGB'))
    brightened_image = enhancer.enhance(display_brightness)
    matrix.SetImage(brightened_image)

if len(sys.argv) == 2:
    # Display image mode, usually used for debugging or manual control
    print("Displaying single image")
    image = Image.open(sys.argv[1])

    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height))

    matrix.SetImage(image.convert('RGB'))

    print("Press CTRL-C to stop.")
    while True:
        matrix.SetImage(image.convert('RGB'))
        time.sleep(0.05)
else:
    # Get text display ready
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/7x14.bdf")
    # Get designs from external folder
    submissions_config = json.load(open(config["submissionsDirectory"] + "/submissions.json"))
    submissions = submissions_config["submissions"]
    design_duration = config["designDuration"]
    message_duration = config["messageDuration"]
    updates_per_submission = config["updatesPerSubmission"]
    submission_index = -1
    while True:
        if "relayHost" in config and not connected:
            if submission_index % 3 == 0 and connected_to_internet():
                print("Internet connected, trying to connect to relay server")
                try_to_connect()
            elif submission_index == 0:
                # Just in case there is something wrong with my internet detection code
                print("Not detecting internet connection, giving it the ol' college try anyways")
                try_to_connect()

        if display_override is None:
            submission_index += 1
            submission = submissions[submission_index % len(submissions)]
            if not "design" in submission and "message" in submission:
                offscreen_canvas.Clear()
                position = offscreen_canvas.width
                while True:
                    if display_override is not None:
                        break
                    offscreen_canvas.Clear()
                    textColor = graphics.Color(0 * display_brightness, 255 * display_brightness, 255 * display_brightness)
                    text_length = graphics.DrawText(offscreen_canvas, font, position, 22, textColor, submission["message"])
                    position -= 1
                    if (position + text_length < 0):
                        break
                    time.sleep(message_duration / text_length)
                    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
            else:
                updates_left = updates_per_submission
                while updates_left > 0 and display_override is None:
                    display_image(config["submissionsDirectory"] + "/designs/" + submission["design"])
                    updates_left = updates_left - 1
                    time.sleep(design_duration / updates_per_submission)
        else:
            if display_override >= 0 and display_override < len(submissions):
                submission = submissions[display_override]
                display_image(config["submissionsDirectory"] + "/designs/" + submission["design"])
                time.sleep(design_duration / updates_per_submission)
            else:
                display_override = None
                print("Error: Display override of " + str(display_override) + " is out of bounds") 