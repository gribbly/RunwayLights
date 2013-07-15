'''
Alt for Patterns.py that treats led string as two "sides", etc.
'''

import sys
import math
import time
from random import randint

sides = [] #whole string
side1 = [] #e.g, 0-12 (first half)
side2 = [] #e.g, 13-25 (second half)
rcIndex = 0

def log_event(msg):
	print sys.argv[0] + " - " + msg	

def create(ledStrip):
	global side1, sides2, sides, rcIndex
	log_event('create sides from {0} leds'.format(ledStrip.nLeds))
	realLength = ledStrip.nLeds
	length1 = realLength / 2
	log_event('length1 is {0}'.format(length1))
	
	length2 = realLength - length1
	log_event('length2 is {0}'.format(length2))
	
	#initialize sides to off
	for i in range(0,length1):
		side1.append(False)
	for i in range(0,length2):
		side2.append(False)
	#initialize whole string from sides
	sides = side1 + side2
	
	#dump what we got
	log_event('sides has length {0}'.format(len(sides)))
	for i in range(0, len(sides)):
		print i, sides[i]
	
	print "--"

def randomize():
	global side1, side2, sides
	for i in range(0,len(side1)):
		side1[i] = coinToss()
	for i in range(0,len(side2)):
		side2[i] = coinToss()
	sides = side1 + side2
	
def chase():
	global side1, side2, sides, rcIndex
	for i in range(0,len(side1)): #assumes side1 is < side2
		b = False
		if i == rcIndex:
			b = True

		side1[i] = b
		side2[i] = b
	
	rcIndex += 1
	if rcIndex > len(side1):
		rcIndex = 0

	sides = side1 + side2	
	
def update(ledStrip):
	global sides
	for i in range(0, ledStrip.nLeds):
		if sides[i] == False:
			ledStrip.setPixel(i, [0, 0, 0])
		else:
			ledStrip.setPixel(i, [255, 255, 255])
	ledStrip.update()
	time.sleep(0)

def coinToss():
	if randint(0,1) == 0:
		return False
	else:
		return True