#attempt 5 - using queues... original source here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888#437888

#tweaks
nodes = 25
startPattern = 7 #starting pattern
tick = 0.05 #starting tick
fakeMode = False
noServer = False

import sys
import time
if fakeMode == False:
	from LedStrip_WS2801 import LedStrip_WS2801
else:
	from LedStrip_WS2801 import LedStrip_Fake
import Patterns

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

#START
f = open('log','w')
f.write(sys.argv[0] + ' HELLO WORLD @ {0}\n'.format(time.time()))

if fakeMode == False:
	f.write(sys.argv[0] + ' starting in REAL mode\n')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print sys.argv[0] + ' WARNING: fakeMode is True'
	f.write(sys.argv[0] + ' starting in FAKE mode\n')
	ledStrip = LedStrip_Fake(nodes)
	tick = 1.5

pattern = startPattern
if len(sys.argv) > 1:
	try:
		pattern = int(sys.argv[1])
	except:
		print sys.argv[0] + ' WARNING! Bad pattern arg {0}'.format(sys.argv[1])

if noServer == False:
	f.write(sys.argv[0] + ' - starting SuperSimple.py @ {0}\n'.format(time.time()))
	p = Popen(['./SuperSimple.py'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
	q = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t.daemon = True # thread dies with the program
	t.start()
	f.write(sys.argv[0] + ' - started SuperSimple.py @ {0}\n'.format(time.time()))

print sys.argv[0] + ' tick is {0}'.format(tick)
f.write(sys.argv[0] + ' - tick is {0}\n'.format(tick))
print sys.argv[0] + ' pattern is {0}'.format(pattern)
f.write(sys.argv[0] + ' - pattern is {0}\n'.format(pattern))

nextTick = time.time()

f.write(sys.argv[0] + ' - we have {0} ws2801 nodes\n'.format(ledStrip.nLeds))
f.write(sys.argv[0] + ' - clear strip @ {0}\n'.format(time.time()))
Patterns.clearAll(ledStrip)

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
					Patterns.resetSharedVars()

	if time.time() > nextTick:
		#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
		nextTick = time.time() + tick
		#print 'tick: {0}'.format(tick)
		
		if pattern == 0:
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
			Patterns.lightningStringBlink(ledStrip, 33)
		elif pattern == 7:
			Patterns.stringPulsate(ledStrip)
		else:
			print sys.argv[0] + ' WARNING! bad pattern number {0}'.format(pattern)
			f.write(sys.argv[0] + ' WARNING! bad pattern number {0}\n'.format(pattern))
			pattern = 1 #set to something sane