RunwayLights
============

Requires
--------
* Occidentalis v0.2 (unless fakeMode == True)

Instructions
------------
Ensure LEDs are powered, then run **sudo python Flasher.py**

Flasher.py does the following:
* Starts SuperSimple.py (minimalist socket server) in a child thread (use noSocket = True to disable)
* Connects to LED string via GPIO (use fakeMode = True to bypass)
* Writes to a log file (called 'log')
* Then loops indefinitely:
  * Checks to see if SuperSimple has written anything to stdout. If so, process this input (e.g., change tick time or pattern or whatever)
  * Update LED pattern(s)

Note: You can pass a pattern int on the command line:

**sudo python Flasher.py 3**

To connect to the socket server
-------------------------------

(NOTE: We are not running the pi as an access point yet! This requires both the pi and whatever is running websocket.html to be connected to the same network)

1. Load websocket.html in a browser
2. Change the address to ws://raspberrypi.local:8000/
3. Make sure Flasher.py is running
4. Hit "Connect" (should see "connected" in the output)
5. Send protocol commands (see below)


Protocol
--------
pattern=int

bpm=float

light=int

fire=int

...which I'll interpret like this:

* pattern - I'll immediately switch to the specified pattern number (suggest we use ints not pattern names). Let's reserve pattern=0 for "everything off"
* bpm - pattern tempo in beats-per-minute. I will calculate tick from this.
* light - turn on a specific light (in addition to current pattern)
* fire - turn on a specific fire (in addition to current pattern)

If we need to handle multiple parameters per message, comma separate them:

pattern=1,tick=0.5

Troubleshooting:
----------------
* If Flasher.py crashes you may need to kill the server manually before restarting. Get PID from **ps -A | grep Super** then do **sudo kill PID**.

Workflow Notes
--------------
Git:
**git pull origin master**
**git add FILE**
**git commit -a** (then save commit message via nano)
**git push**


