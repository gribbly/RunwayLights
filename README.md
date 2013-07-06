RunwayLights
============

Requires
--------
* Occidentalis v0.2

Instructions
------------
Ensure LEDs are powered, then run **sudo python Flasher.py**

Flasher.py does the following:
* Starts SuperSimple.py (minimalist socket server) in a child thread
* Connects to LED string via GPIO
* Writes to a log file (called 'log')
* Then loops indefinitely:
  * Checks to see if SuperSimple has written anything to stdout. If so, process this input (e.g., change tick time or pattern or whatever)
  * Update LED pattern(s)

To connect to the socket server
-------------------------------

(NOTE: We are not running the pi as an access point yet! This requires both the pi and whatever is running websocket.html to be connected to the same network)

1. Load websocket.html in a browser
2. Change the address to ws://raspberrypi.local:8000/
3. Make sure Flasher.py is running
4. Hit "Connect" (should see "connected" in the output)
5. No enter numbers (like 0.1, 1.0, 3.0) and hit "Send"
 1. Valid numbers should change the tick time
 2. Invalid input - you'll see NaN in the stdout of Flasher.py
 

Troubleshooting:
----------------
* If you can't connect to the socket, try **ps -A | grep Super** and ensure that Flasher.py has launched SuperSimple.py 
