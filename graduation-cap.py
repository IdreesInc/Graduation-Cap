#!/usr/bin/env python
import time
import sys
import json
import socketio

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

matrix = RGBMatrix(options = options)

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit("graduation-cap-connected", "I'm in")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def brightness(data):
    global display_brightness
    print('Message received, brightness -> ' + data)
    display_brightness = float(data) / 100


if "relayHost" in config:
    try:
        sio.connect(config["relayHost"])
    except Exception:
        print("Error while trying to connect to socketio server, proceeding to get on with life")

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
    submission_index = -1
    while True:
        submission_index += 1
        submission = submissions[submission_index % len(submissions)]
        if not "design" in submission and "message" in submission:
            offscreen_canvas.Clear()
            position = offscreen_canvas.width
            while True:
                offscreen_canvas.Clear()
                textColor = graphics.Color(0 * display_brightness, 255 * display_brightness, 255 * display_brightness)
                text_length = graphics.DrawText(offscreen_canvas, font, position, 22, textColor, submission["message"])
                position -= 1
                if (position + text_length < 0):
                    break

                time.sleep(message_duration / text_length)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        else:
            image = Image.open(config["submissionsDirectory"] + "/designs/" + submission["design"])
            image.thumbnail((matrix.width, matrix.height))
            enhancer = ImageEnhance.Brightness(image.convert('RGB'))
            brightened_image = enhancer.enhance(display_brightness)
            matrix.SetImage(brightened_image)
            time.sleep(design_duration)