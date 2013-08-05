import sys
import math
import time
from random import randint

sharedBool = False
sharedIndex = 0
sharedInt = 0
sleepTime = 0

def resetSharedVars():
	global sharedBool
	global sharedIndex
	global sharedInt
	sharedBool = False
	sharedIndex = 0
	sharedInt = 0

def clearAll(ledStrip):
	global sleepTime
	for i in range(0, ledStrip.nLeds):
		ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(sleepTime)
	
def randomString(ledStrip):
	global sleepTime
	for i in range(0, ledStrip.nLeds):
		if randint(0,1) == 0:
			ledStrip.setPixel(i, [0, 0, 0])
		else:
			ledStrip.setPixel(i,[255, 255, 255])
	ledStrip.update()
	time.sleep(sleepTime)

def randomPoint(ledStrip):
	global sleepTime
	p = randint(0, ledStrip.nLeds)
	for i in range(0, ledStrip.nLeds):
		if i == p:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(sleepTime)
	
def simpleChaser(ledStrip):
	global sleepTime
	global sharedIndex
	p = sharedIndex
	sharedIndex += 1
	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = 0
	for i in range(0, ledStrip.nLeds):
		if i == p:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(sleepTime)
	
def cylonChaser(ledStrip):
	global sleepTime
	global sharedBool
	global sharedIndex

	if sharedBool == False:
		sharedIndex += 1
	else:
		sharedIndex -= 1

	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = ledStrip.nLeds - 1
		sharedBool = True
	if sharedIndex < 0:
		sharedIndex = 0
		sharedBool = False

	for i in range(0, ledStrip.nLeds):
		if (i == sharedIndex):
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(sleepTime)
	
def stringBlink(ledStrip):
	global sleepTime
	global sharedBool
	b = sharedBool
	for i in range(0, ledStrip.nLeds):
		if b == True:
			ledStrip.setPixel(i,[255, 255, 255])
			sharedBool = False
		else:
			ledStrip.setPixel(i, [0, 0, 0])
			sharedBool = True
	ledStrip.update()
	time.sleep(sleepTime)

def lightningStringBlink(ledStrip, probability):
	global sleepTime
	c = randint(0,100)
	for i in range(0, ledStrip.nLeds):
		if c < probability:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(sleepTime)

def stringPulsate(ledStrip):
	global sleepTime
	global sharedBool
	global sharedInt
	if sharedBool == False:
		sharedInt += 1
	else:
		sharedInt -= 1	

	if sharedInt > 255:
		sharedInt = 255
		sharedBool = True
	if sharedInt < 0:
		sharedInt = 0
		sharedBool = False	
	
	for i in range(0, ledStrip.nLeds):
		ledStrip.setPixel(i,[sharedInt, sharedInt, sharedInt])
	ledStrip.update()
	time.sleep(sleepTime)

def watery(ledStrip, intensity):
	global sleepTime
	t = time.clock()
	for i in range(0, ledStrip.nLeds):
		p = math.sin(t + i)
		p = abs(p) * intensity
		p = int(p)
		#print p
		ledStrip.setPixel(i,[p, p, p])
	ledStrip.update()
	time.sleep(sleepTime)

def blueWatery(ledStrip, intensity):
	global sleepTime
	t = time.clock()
	for i in range(0, ledStrip.nLeds):
		p = math.sin(t + i)
		p = abs(p) * intensity
		p = int(p)
		#print p
		ledStrip.setPixel(i,[0, p, 0])
	ledStrip.update()
	time.sleep(sleepTime)
