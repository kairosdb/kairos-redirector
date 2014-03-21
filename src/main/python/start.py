import sys
import os
import os.path
import ConfigParser
from kairos import redirector
from kairos.uploader import Uploader

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
if (os.path.exists(fifoPath)):
	os.remove(fifoPath)

os.mkfifo(fifoPath)

#register signal handler


#callinto pipe reader
upload = Uploader(kairosUrl)




#remove named pipe
os.remove(fifoPath)

print "Exiting"
