#attempt 5 - using queues... original source here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888#437888

#tweaks
nodes = 25
pattern = 7 #starting pattern
tick = 0.05 #starting tick
fakeMode = False

import sys
import math
import time
from random import randint
if fakeMode == False:
	from LedStrip_WS2801 import LedStrip_WS2801
else:
	from LedStrip_WS2801 import LedStrip_Fake

# queues
from subprocess import PIPE, Popen
from threading  import Thread
from Queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
# /queues

def clearAll(ledStrip):
	for i in range(0, ledStrip.nLeds):
		ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(0)
	
def randomString(ledStrip):
	for i in range(0, ledStrip.nLeds):
		if randint(0,1) == 0:
			ledStrip.setPixel(i, [0, 0, 0])
		else:
			ledStrip.setPixel(i,[255, 255, 255])
	ledStrip.update()
	time.sleep(0)

def randomPoint(ledStrip):
	p = randint(0, ledStrip.nLeds)
	for i in range(0, ledStrip.nLeds):
		if i == p:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(0)
	
def simpleChaser(ledStrip):
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
	time.sleep(0)
	
def cylonChaser(ledStrip):
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
	time.sleep(0)
	
def stringBlink(ledStrip):
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
	time.sleep(0)

def lightningStringBlink(ledStrip, probability):
	c = randint(0,100)
	for i in range(0, ledStrip.nLeds):
		if c < probability:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	ledStrip.update()
	time.sleep(0)

def stringPulsate(ledStrip):
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
	time.sleep(0)	

#START
f = open('log','w')
f.write(sys.argv[0] + ' HELLO WORLD @ {0}\n'.format(time.time()))

#globals (don't change these)
sharedBool = False
sharedIndex = 0
sharedInt = 0

if fakeMode == False:
	f.write(sys.argv[0] + ' starting in REAL mode\n')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print sys.argv[0] + ' WARNING: fakeMode is True'
	f.write(sys.argv[0] + ' starting in FAKE mode\n')
	ledStrip = LedStrip_Fake(nodes)
	tick = 1.5

if len(sys.argv) > 1:
	tick = float(sys.argv[1])
f.write(sys.argv[0] + ' - starting SuperSimple.py @ {0}\n'.format(time.time()))

# queues
p = Popen(['./SuperSimple.py'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()
# /queues

f.write(sys.argv[0] + ' - started SuperSimple.py @ {0}\n'.format(time.time()))

print sys.argv[0] + ' tick is {0}'.format(tick)
f.write(sys.argv[0] + ' - tick is {0}\n'.format(tick))
print sys.argv[0] + ' pattern is {0}'.format(pattern)
f.write(sys.argv[0] + ' - pattern is {0}\n'.format(pattern))

nextTick = time.time()

f.write(sys.argv[0] + ' - we have {0} ws2801 nodes\n'.format(ledStrip.nLeds))
f.write(sys.argv[0] + ' - clear strip @ {0}\n'.format(time.time()))
clearAll(ledStrip)

while True:	
	try:  line = q.get_nowait() # or q.get(timeout=.1)
	except Empty:
		tmp = 0
	else: # got line
		input = str(line).split(',')
		command = input[0].split('=')
		if command[0] == 'tick':
			try: 
				print('Got tick command')
				f.write('Got tick command\n')
				tick = float(command[1].rstrip())
			except:
				print('Bad tick input: ' + str(line))
				f.write('Bad tick input: ' + str(line) + '\n')
			else:
				print('Tick update:' + str(tick))
				f.write('Tick update: ' + str(tick) + '\n')
		elif command[0] == 'pattern':
			try: 
				print('Got pattern command')
				f.write('Got pattern command\n')
				pattern = int(command[1].rstrip())
			except:
				print('Bad pattern input: ' + str(line))
				f.write('Bad pattern input: ' + str(line) + '\n')
			else:
				print('Pattern update:' + str(pattern))
				f.write('Pattern update: ' + str(pattern) + '\n')
				sharedBool = False
				sharedIndex = 0
				sharedInt = 0

	if time.time() > nextTick:
		#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
		nextTick = time.time() + tick
		#print 'tick: {0}'.format(tick)
		
		if pattern == 0:
			clearAll(ledStrip)
		elif pattern == 1:
			randomString(ledStrip)
		elif pattern == 2:
			randomPoint(ledStrip)
		elif pattern == 3:
			simpleChaser(ledStrip)
		elif pattern == 4:
			cylonChaser(ledStrip)
		elif pattern == 5:
			stringBlink(ledStrip)	
		elif pattern == 6:			
			lightningStringBlink(ledStrip, 33)
		elif pattern == 7:
			stringPulsate(ledStrip)