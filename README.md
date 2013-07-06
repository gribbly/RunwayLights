RunwayLights
============

Requires
--------
* Occidentalis v0.2 (unless fakeMode == True)

Instructions
------------
Ensure LEDs are powered, then run **sudo python Flasher.py**

Flasher.py does the following:
* Starts SuperSimple.py (minimalist socket server) in a child thread
* Connects to LED string via GPIO (use fakeMode = True to bypass)
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
* If you need to kill the socket server, get PID from above then **sudo kill <pid>**

Protocol
--------
pattern=<int>
tick=<float>
finger1=<float>
finger2=<float>

...which I'll interpret like this:

pattern// I'll immediately switch to the specified pattern number (suggest we use ints not pattern names). Let's reserve pattern=0 for "everything off"
tick //tick time in seconds (so 1.0 means one second between pattern updates)
finger1 //send me a float from 0.0 to 1.0 representing how far along the string the user is pressing. So 0.5 for "halfway along". This means we can vary the number of nodes in the string if necessary without breaking anything later. Finger input will override any underlying pattern.
finger2 //as for finger1

If we need to handle multiple parameters per message, comma separate them:

pattern=1,tick=0.5

