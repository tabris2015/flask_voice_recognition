from subprocess import Popen, PIPE
import thread

def listen(pocketsphinx):
	print "leyendo la salida"
	while True:
		line = pocketsphinx.stdout.readline()
		print line

print "start"
command = 'pocketsphinx_continuous -backtrace yes -inmic yes'
pocketsphinx = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)  
thread.start_new_thread(listen, (pocketsphinx,))

c = raw_input("Type something to quit.")