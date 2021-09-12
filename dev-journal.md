# Dev Journal

## September 10th, 2021

- Started work on the client interface, beginning with the LED matrix canvas.
- Had some trouble getting the tap events to register properly and getting the drawing with drag working. Tapping to draw was easy enough, but making it possible to drag your finger/mouse across the screen and have the underlying LED elements become filled in was harder.
  - Required some flimsy event listeners on the actual matrix rather than individual LED elements which is annoying, but seems to work fine for now.
- Next up is to get the Python webserver working, then to make it possible to edit the board, then to add more tools for drawing.

## September 7th, 2021

- Messing around with the sample python scripts, looks like I can get a stable 20 fps at least by using the SetImage command. That should be more than enough and means that the matrix shouldn't be the bottleneck.