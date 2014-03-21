#! /usr/bin/env python

import urllib2
import os

class File2(file):
    def __init__(self, *args, **keyws):
        file.__init__(self, *args, **keyws)

    def __len__(self):
        return int(os.fstat(self.fileno())[6])

kdbUrl = 'http://10.92.0.14:8080/api/v1/datapoints'
inputFile = 'input.json'

jsonData = """[{
        'name' : 'test_point1',
        'timestamp' : 1395422539,
        'value' : 123,
        'tags' : { 'host' : 'pk' }
    }]"""

fileData = File2(inputFile, 'r')

print "Url: " + kdbUrl

req = urllib2.Request(kdbUrl)
req.add_header('Content-Type', 'application/json')

res = urllib2.urlopen(req, fileData)

for l in res:
    print l
