# Dev Journal

## September 12th, 2021

- Trying to decide between Python 2.7 vs 3, but it isn't as clearcut as I'd like. Obviously it'd be preferable to use 3, but the rpi-rgb-led-matrix library that is the core of this project mentions that using Python 2.7 with the library is a little bit faster. Testing it on my own shows that Python 3 is only a little slower, so I am going to stick with it for now and if speed becomes a bottleneck I will reconsider once we get there.
- Wait, is the webserver even necessary? I obviously need something to present the client interface, but that service can be provided by any old host.
  - If I instead use a relay server and make the hat run a WebSocket client instead, then I can offload a significant amount of load to the relay and make sure the hat doesn't have to deal with dozens of simultaneous connections.
  - Another benefit is that I don't have to worry about security with regards to the Python webserver and can instead use a static host like GitHub Pages.
- Created Helios-Relay, which will run the relay code.
- Turns out WebSockets are messy and I am short on time. Let's use Socket.IO and skip all of that mess.

## September 10th, 2021

- Started work on the client interface, beginning with the LED matrix canvas.
- Had some trouble getting the tap events to register properly and getting the drawing with drag working. Tapping to draw was easy enough, but making it possible to drag your finger/mouse across the screen and have the underlying LED elements become filled in was harder.
  - Required some flimsy event listeners on the actual matrix rather than individual LED elements which is annoying, but seems to work fine for now.
- Next up is to get the Python webserver working, then to make it possible to edit the board, then to add more tools for drawing.

## September 7th, 2021

- Messing around with the sample python scripts, looks like I can get a stable 20 fps at least by using the SetImage command. That should be more than enough and means that the matrix shouldn't be the bottleneck.