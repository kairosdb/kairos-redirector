#! /usr/bin/env python

import urllib2
import os
import gzip

class File2(file):
    def __init__(self, *args, **keyws):
        file.__init__(self, *args, **keyws)

    def __len__(self):
        return int(os.fstat(self.fileno())[6])

class Uploader:
    def __init__(self, url):
        self.url = url

    def upload(self, filePath, zipIt = True):
        kdbUrl = self.url + '/api/v1/datapoints'

        print 'Url: ' + kdbUrl
        print 'File: ' + filePath

        if (zipIt):
            uploadFilePath = filePath + '.gz'
            contentType = 'application/gzip'
            f_in = open(filePath, 'rb')
            f_out = gzip.open(uploadFilePath, 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
        else:
            uploadFilePath = filePath
            contentType = 'application/json'

        #uploadFile = File2(uploadFilePath, 'r')

        req = urllib2.Request(kdbUrl)
        req.add_header('Content-Type', contentType)

        f = open(uploadFilePath, 'r')
        contents = f.read()
        f.close()
        
        print contents
        
        exitCode = False
        try:
            res = urllib2.urlopen(req, contents)
            

            print 'Response code: ' + str(res.code)

            for l in res:
                print l
    
            if res.code == 204:
                exitCode = True
            else:
                exitCode = False

        except urllib2.HTTPError, e:
            print("Error: %s" % e)
            print("Code: %s" % e.code)
            if e.code == 204:
                exitCode = True

        except urllib2.URLError, e:
            print("Error: %s" % e)
            print(e.args)

        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print ( "Error: %s" % e )

        return exitCode
