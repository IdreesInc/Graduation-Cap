#!/usr/bin/env python
# Display a runtext with double-buffering.
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import sys

my_text = "Hello, world!"
if len(sys.argv) >=2:
    my_text = sys.argv[1]

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.brightness = 90

matrix = RGBMatrix(options = options)

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("./fonts/7x14.bdf")
textColor = graphics.Color(0, 255, 255)
pos = offscreen_canvas.width

print("Press CTRL-C to stop.")
while True:
    offscreen_canvas.Clear()
    len = graphics.DrawText(offscreen_canvas, font, pos, 22, textColor, my_text)
    pos -= 1
    if (pos + len < 0):
        pos = offscreen_canvas.width

    time.sleep(0.025)
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)