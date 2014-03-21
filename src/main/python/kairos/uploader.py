#! /usr/bin/env python

import urllib2
import os

class File2(file):
    def __init__(self, *args, **keyws):
        file.__init__(self, *args, **keyws)

    def __len__(self):
        return int(os.fstat(self.fileno())[6])

class uploader():
    def __init__(self, url):
        self.url = url

    def upload(self, filePath, zipIt = False):
        kdbUrl = self.url + '/api/v1/datapoints'

        print 'Url: ' + kdbUrl
        print 'File: ' + filePath

        uploadFile = File2(filePath, 'r')

        req = urllib2.Request(kdbUrl)
        req.add_header('Content-Type', 'application/json')

        res = urllib2.urlopen(req, uploadFile)

        for l in res:
            print l
