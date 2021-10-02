#!/usr/bin/env python
import time
import sys
import json

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

config = json.load(open("./config.json"))
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = config["brightness"]

matrix = RGBMatrix(options = options)

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
    print("Starting graduation cap")
    # Get text display ready
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("./fonts/7x14.bdf")
    textColor = graphics.Color(0, 255, 255)
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
                text_length = graphics.DrawText(offscreen_canvas, font, position, 22, textColor, submission["message"])
                position -= 1
                if (position + text_length < 0):
                    break

                time.sleep(message_duration / text_length)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        else:
            image = Image.open(config["submissionsDirectory"] + "/designs/" + submission["design"])
            image.thumbnail((matrix.width, matrix.height))
            matrix.SetImage(image.convert('RGB'))
            time.sleep(design_duration)