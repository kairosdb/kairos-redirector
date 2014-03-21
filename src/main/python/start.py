import sys
import os
import ConfigParser
from kairos import redirector

print "Sarting up"

if (len(sys.argv) != 2):
	print 'You must provide a path to the redirector.ini!'
	sys.exit(1);
	
configPath = sys.argv[1]

config = ConfigParser.ConfigParser()
config.read(configPath)

kairosUrl = config.get('main', 'KairosURL')
fifoPath = config.get('main', 'fifo_path')

print kairosUrl
print fifoPath

#create named pipe
#todo: should check if the file is there, delete it and then create it
os.mkfifo(fifoPath)

#register signal handler


#callinto pipe reader



#remove named pipe
os.remove(fifoPath)

print "Exiting"
