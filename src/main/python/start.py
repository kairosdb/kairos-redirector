import sys
import ConfigParser
from kairos import redirector

print "Sarting up"

if (len(sys.argv) != 2):
	print 'You must provide a path to the redirector.ini!'
	sys.exit(1);
	
configPath = sys.argv[1]

config = ConfigParser.ConfigParser()
config.read(configPath)

print config.get('main', 'KairosURL')
print config.get('main', 'fifo_path')

#todo: read from config file to get kairos location
# read location of named pipe

#create named pipe

#register signal handler


#callinto pipe reader

#remove named pipe

print "Exiting"
