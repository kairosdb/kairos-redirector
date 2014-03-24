import sys
import os
import os.path
import ConfigParser
from kairos import redirector
from kairos.uploader import Uploader
from kairos import reader

print "Sarting up"

if (len(sys.argv) != 2):
	print 'You must provide a path to the redirector.ini!'
	sys.exit(1)
	
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
os.chmod(fifoPath, 0666)

#register signal handler


#callinto pipe reader
upload = Uploader(kairosUrl)


reader.reader(upload, fifoPath)
os.remove(fifoPath)

print "Exiting"
