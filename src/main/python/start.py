#!/usr/bin/python

import sys
import os
import os.path
import ConfigParser
import signal
from kairos.uploader import Uploader
from kairos.reader import Reader


def handler(signum, frame):
    global reader
    print "Exiting"
    reader.stop()


print "Starting up"

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

#callinto pipe reader
upload = Uploader(kairosUrl)

reader = Reader(upload, fifoPath)

#register signal handler
signal.signal(signal.SIGINT, handler)
signal.pause()

reader.join()
os.remove(fifoPath)
print "Exiting"
