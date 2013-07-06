RunwayLights
============

Requires: 
* Occidentalis v0.2

Instructions:
* sudo python Flasher.py

Flasher.py does the following:
* Starts SuperSimple.py (minimalist socket server) in a child thread
* Connects to LED string via GPIO
* Writes to a log file (called 'log')
* Then loops indefinitely:
  * Checks to see if SuperSimple has written anything to stdout. If so, process this input (e.g., change tick time or pattern or whatever)
  * Update LED pattern(s)
