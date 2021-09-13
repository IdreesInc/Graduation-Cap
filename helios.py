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
matrix_options.hardware_mapping = "adafruit-hat"
matrix_options.brightness = 90

matrix = RGBMatrix(options = matrix_options)

image = Image.open(config["splash"])
image.thumbnail((matrix.width, matrix.height))
image = image.convert("RGB")
matrix.SetImage(image)

def rotate(angle):
    global image
    print("Rotating to {}".format(angle))
    image = image.rotate(90)
    matrix.SetImage(image, 0, 0, False)

def draw_on_matrix(x, y):
    global image
    print("Drawing at x: {} y: {}".format(x, y))
    image.putpixel((x, y), (255, 0, 0, 255))
    matrix.SetImage(image, 0, 0, False)

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(data):
    print('I received a message!')
    print(data["text"])

@sio.event
def transform(data):
    print('Transformation Received')
    print(data)
    if data["operation"] == "rotate":
        rotate(data["angle"])

@sio.event
def draw(data):
    print('Draw Command Received')
    print(data)
    for coordinates in data:
        draw_on_matrix(coordinates[0], coordinates[1])

sio.connect(config["host"])
