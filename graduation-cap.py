#!/usr/bin/env python
import time
import sys
import json

from rgbmatrix import RGBMatrix, RGBMatrixOptions
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
    submissions_config = json.load(open(config["submissionsDirectory"] + "/submissions.json"))
    submissions = submissions_config["submissions"]
    default_delay = config["defaultDelay"]
    submission_index = -1
    while True:
        submission_index += 1
        submission = submissions[submission_index % len(submissions)]
        if not "design" in submission:
            # Message, will deal with later
            continue
        image = Image.open(config["submissionsDirectory"] + "/designs/" + submission["design"])
        image.thumbnail((matrix.width, matrix.height))
        matrix.SetImage(image.convert('RGB'))
        time.sleep(default_delay)