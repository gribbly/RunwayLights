#attempt 5 - using queues... original source here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888#437888

fakeMode = True

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



#START
f = open('log','w')
f.write(sys.argv[0] + ' HELLO WORLD @ {0}\n'.format(time.time()))

tick = 0.05
nodes = 25

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

nextTick = time.time()

f.write(sys.argv[0] + ' - we have {0} ws2801 nodes\n'.format(ledStrip.nLeds))
f.write(sys.argv[0] + ' - clear strip @ {0}\n'.format(time.time()))
clearAll(ledStrip)

while True:	
	try:  line = q.get_nowait() # or q.get(timeout=.1)
	except Empty:
		tmp = 0
	else: # got line
		try: tick = float(line)
		except:
			print('Nan')
		else:
			print('Tick update:' + str(line))
			f.write(str(line) + '\n')

	if time.time() > nextTick:
		#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
		nextTick = time.time() + tick
		#print 'tick: {0}'.format(tick)
		randomString(ledStrip)