#!/usr/bin/env python3

import time
import sys

import json
import socketio
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

print("Starting Helios!")

config = json.load(open("./config.json"))

# Configuration for the matrix
matrix_options = RGBMatrixOptions()
matrix_options.rows = 32
matrix_options.chain_length = 1
matrix_options.parallel = 1
matrix_options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
matrix_options.brightness = 90

matrix = RGBMatrix(options = matrix_options)

image = Image.open(config["splash"])
# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height))
matrix.SetImage(image.convert('RGB'))

sio = socketio.Client()

@sio.event
def message(data):
    print('I received a message!')
    print(data["text"])

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect(config["host"])
