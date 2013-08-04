#attempt 5 - using queues... original source here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888#437888

#tweaks
nodes = 9
startPattern = 4 #starting pattern
bpm = 120 #default bpm (not used)
tick = 0.1 #starting tick
fakeMode = False
noServer = True
useRunwayControl = False

#/steve test
sliderIdx = 0

import sys
import time
if fakeMode == False:
	from LedStrip_WS2801 import LedStrip_WS2801
else:
	from LedStrip_WS2801 import LedStrip_Fake
import Patterns
import RunwayControl

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

def log_event(msg):
	f.write(sys.argv[0] + " - " + msg + "\n")
	print sys.argv[0] + " - " + msg	

#START
f = open('log','w')
log_event(' HELLO WORLD @ {0}'.format(time.time()))

if fakeMode == False:
	log_event(' starting in REAL mode')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print '*** WARNING: fakeMode is True ***'
	log_event('starting in FAKE mode')
	ledStrip = LedStrip_Fake(nodes)
	tick = .5

pattern = startPattern
if len(sys.argv) > 1:
	try:
		pattern = int(sys.argv[1])
	except:
		log_event('WARNING! Bad pattern arg {0}'.format(sys.argv[1]))
if useRunwayControl == True:
	pattern = -1

if noServer == False:
	log_event('starting SuperSimple.py @ {0}'.format(time.time()))
	p = Popen(['/home/pi/Flasher4/SuperSimple.py'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
	q = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t.daemon = True # thread dies with the program
	t.start()
	log_event('started SuperSimple.py @ {0}'.format(time.time()))

log_event('tick is {0}'.format(tick))
log_event('pattern is {0}'.format(pattern))

nextTick = time.time()

log_event('we have {0} ws2801 nodes'.format(ledStrip.nLeds))
log_event('clear strip @ {0}'.format(time.time()))
Patterns.clearAll(ledStrip)

if useRunwayControl == True:
	RunwayControl.create(ledStrip)



while True:	
	if noServer == False:
		try:  line = q.get_nowait() # or q.get(timeout=.1)
		except Empty:
			tmp = 0
		else: # got line
			input = str(line).split(',')
			command = input[0].split('=')
			if command[0] == 'tick':
				try: 
					log_event('Got tick command')
					tick = float(command[1].rstrip())
				except:
					log_event('Bad tick input: ' + str(line))
				else:
					log_event('Tick update:' + str(tick))
			elif command[0] == 'bpm':
				try: 
					log_event('Got bpm command')
					bpm = float(command[1].rstrip())
				except:
					log_event('Bad bpm input: ' + str(line))
				else:
					log_event('Bpm update:' + str(float(command[1].rstrip())))
			elif command[0] == 'pattern':
				try: 
					log_event('Got pattern command')
					pattern = int(command[1].rstrip())
				except:
					log_event('Bad pattern input: ' + str(line))
				else:
					log_event('Pattern update:' + str(pattern))
					if useRunwayControl == false:
						Patterns.resetSharedVars()
			elif command[0] == 'light':
				try: 
					log_event('Got light command')
				except:
					log_event('Bad light input: ' + str(line))
				else:
					log_event('Light update:' + str(float(command[1].rstrip())))
			elif command[0] == 'fire':
				try: 
					log_event('Got fire command')
				except:
					log_event('Bad fire input: ' + str(line))
				else:
					log_event('Fire update:' + str(float(command[1].rstrip())))

	if time.time() > nextTick:
		#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
		nextTick = time.time() + tick
		#print 'tick: {0}'.format(tick)
		
		if useRunwayControl == True:
#			RunwayControl.chase2()
			#/steve
			# temp code, surrogate for osc slider input
			sliderIdx = sliderIdx+1
			if sliderIdx>14:
				sliderIdx = 0
			RunwayControl.slider(sliderIdx)
			RunwayControl.update(ledStrip)
		
		if pattern == -1:
			tmp = 0
		elif pattern == 0:
			Patterns.clearAll(ledStrip)
		elif pattern == 1:
			Patterns.randomString(ledStrip)
		elif pattern == 2:
			Patterns.randomPoint(ledStrip)
		elif pattern == 3:
			Patterns.simpleChaser(ledStrip)
		elif pattern == 4:
			Patterns.cylonChaser(ledStrip)
		elif pattern == 5:
			Patterns.stringBlink(ledStrip)	
		elif pattern == 6:			
			Patterns.lightningStringBlink(ledStrip, 33) #probability
		elif pattern == 7:
			Patterns.stringPulsate(ledStrip)
		elif pattern == 8:
			Patterns.watery(ledStrip, 128) #intensity
		elif pattern == 9:
			Patterns.blueWatery(ledStrip, 128) #intensity
		else:
			log_event('WARNING! bad pattern number {0}'.format(pattern))
			pattern = 1 #set to something sane
