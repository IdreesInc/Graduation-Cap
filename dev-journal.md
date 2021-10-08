# Dev Journal

## October 7th, 2021

- Increased the update rate of the display.
- Added retry logic for the relay server initial connection. That way if the cap isn't connected on the first startup, it can try again.
- Made the design overrides indefinite with a command to release control.

## October 6th, 2021

- Added the ability to view the graduation cap's connection status in the client controller webapp.
  - One thing I found interesting was that I had to remember to pass on whether the grad cap was connected to new client connections as well, otherwise they'd miss the broadcast that occurs when the cap first connects.
  - It's really satisfying being able to kill the grad cap script, watch the status switch to disconnected, run the script again, and then see the status switch back to connected without having to refresh the client page at all.
- Added the ability to override the image currently being displayed on the cap.
  - While the feature works, it only overrides the image for 10 seconds. Could do to add a customizable timeout there.
- It'd be nice if updates to settings were reflected faster, might want to reduce the time.sleep and instead use timestamps to determine when to go to the next submission.
- To-Do
  - Control brightness ✅
  - Override image selection ✅
  - Custom image override duration
  - Quick refreshes
  - Trigger git pulls
  - Trigger Pi restart (maybe)

## October 5th, 2021

- Got the brightness control via the relay server up and running! Turns out it was a bit harder to control the brightness than I thought. The matrix options are set when the matrix is initialized and there are no functions I can find to modify the settings after the fact. And changes to the options later are not reflected on the matrix. Instead, I update the brightness of the image itself which works well enough. The only side effect is that the brightness only takes effect once the next design is displayed, but I'll take it.
- I am seeing a lot more slowdown on the Pi however, and I am concerned that the websocket client along with the matrix controls are using a lot of resources. I'll have to keep an eye on this as the project progresses. I'll also have to see how battery resources are affected.
- Current to-do list:
  - Brightness ✅
  - Image selection
  - Update submissions
  - Restart Pi

## October 3rd, 2021

- So, if I want to create a command and control server still, then the first thing I should probably figure out is what I actually want to control. Let's list em off:
  - Brightness
  - Image override - basically I want the ability to choose what image to display before letting the "slideshow" continue
  - Git pull the submissions repo
  - Restart the whole bloody thing
- That's probably about it. The brightness thing is easy, just change the in-memory setting after getting a message. Git pull is probably as easy as using some python module that executes shell commands. Restarting the Raspberry Pi is just as easy, though if I just want to restart the server that might be harder (maybe execute a combined kill and python command?). The image override will be the hardest thing to program, but it is also the most important. We will see how that goes.

## October 2nd, 2021

- Gave it some _more_ thought, and decided excluding the relay server is the easy and boring move.
  - I thought making the script capable of going through images one by one and making everything configurable might be difficult, but it turned out to be way too easy!
  - So the node.js relay control server is back on! It'll be a "stretch goal", after I complete the message display thing (which will be difficult because I basically have to design a font but whatever)

## September 29th, 2021

- I've been giving it some thought, and I am starting to realize that maybe relying on the Raspberry Pi to be able to connect to wifi isn't such a great idea.
  - Even with a hotspot, I can't be sure that the connection won't be finnicky and randomly fail during critical minutes.
  - Also with the canvas editor mostly scrapped as part of this project, there really isn't any need to make sure the hat is connected 24/7.
  - It would be nice to be able to control the hat via my phone, but honestly setting up ngrok is probably enough for what I need to do.
- To make sure that the submissions can be updated easily, I have created a separate repository for them. On startup, I can run a git pull to update the designs assuming that the Pi is able to connect to the internet. This way if I ever want to update the designs, I would only need to restart the Pi physically. And since the designs are stored locally, there would be no need for constant internet access.
- Should something go really wrong, I can hopefully use something like ngrok to fix whatever breaks assuming I still have an internet connection.
- Starting to think I might want to do a trial run at UNC beforehand...
- Current todo list:
  - Display images one by one
  - Display scrolling text messages
  - Allow for configuration over a config file
  - Create bash scripts to change settings easily over ssh and restart the python process

## September 27th, 2021

- Now that the graduation cap project has gone public, time for me to clean things up a bit!
- Renaming everything from the internal name "Helios" to just "Graduation Cap" so that it is more visible to people searching for the source code.
- Removing canvas code for now.
  - Since the focus has switched from a public canvas to a public billboard, I am going to set aside the canvas stuff for a later date to prioritize creating a robust system for displaying images and messages.

## September 12th, 2021

- Trying to decide between Python 2.7 vs 3, but it isn't as clearcut as I'd like. Obviously it'd be preferable to use 3, but the rpi-rgb-led-matrix library that is the core of this project mentions that using Python 2.7 with the library is a little bit faster. Testing it on my own shows that Python 3 is only a little slower, so I am going to stick with it for now and if speed becomes a bottleneck I will reconsider once we get there.
- Wait, is the webserver even necessary? I obviously need something to present the client interface, but that service can be provided by any old host.
  - If I instead use a relay server and make the hat run a WebSocket client instead, then I can offload a significant amount of load to the relay and make sure the hat doesn't have to deal with dozens of simultaneous connections.
  - Another benefit is that I don't have to worry about security with regards to the Python webserver and can instead use a static host like GitHub Pages.
- Created Helios-Relay, which will run the relay code.
- Turns out WebSockets are messy and I am short on time. Let's use Socket.IO and skip all of that mess.
- Running into an interesting issue where using SetImage from a python-socketio event callback causes ```OverflowError: can't convert negative value to size_t```. According to a comment on [this](https://github.com/hzeller/rpi-rgb-led-matrix/issues/1056) issue, it is because it is being executed on something other than the main thread. Setting the "unsafe" argument to True fixed the problem, but the updating is a little bit slower. I will consider using [techniques](https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/) for passing messages to the main thread if this becomes a problem.
- Got Socket.IO working on the Python hat server, the Node.js relay server, and the JavaScript web client provided by the relay server. Added basic pixel-by-pixel drawing that is very slow and entirely unoptimized.

## September 10th, 2021

- Started work on the client interface, beginning with the LED matrix canvas.
- Had some trouble getting the tap events to register properly and getting the drawing with drag working. Tapping to draw was easy enough, but making it possible to drag your finger/mouse across the screen and have the underlying LED elements become filled in was harder.
  - Required some flimsy event listeners on the actual matrix rather than individual LED elements which is annoying, but seems to work fine for now.
- Next up is to get the Python webserver working, then to make it possible to edit the board, then to add more tools for drawing.

## September 7th, 2021

- Messing around with the sample python scripts, looks like I can get a stable 20 fps at least by using the SetImage command. That should be more than enough and means that the matrix shouldn't be the bottleneck.