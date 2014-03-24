#!/usr/bin/python
import time


def reader(uploader, pipe):
    metricFile = "./pendingMetrics.json"
    out = open(metricFile, 'w')
    out.write('[')

    #print 'about to open'
    rp = open(pipe, 'r')  # Blocks here until the first message is sent

    metricCount = 0
    done = False
    while not done:
        #print 'About to read' 
        response = rp.readline()
        if not response:
            time.sleep(0.05)
        else:
            metric = response.strip().split(' ')
            
            if (len(metric) < 3):
            	print 'Bad metric '+response
            	continue
            
            print metric

            # todo use Object to encode json
            if metricCount > 0:
                out.write(',')
            out.write('{')
            out.write('"name": "%s",' % metric[0])
            out.write('"timestamp": %s,' % metric[1])
            out.write('"value": %s,' % metric[2])

            out.write('"tags":{')
            tagCount = 0
            for tagString in metric[3:]:
                if tagCount > 0:
                    out.write(',')
                tag = tagString.split('=')
                out.write('"%s": "%s"' % (tag[0], tag[1]))
                tagCount +=1
            out.write('}')

            out.write('}')

            out.flush()
            metricCount += 1

        if metricCount > 1:
            metricCount = 0
            out.write(']')
            out.close()
            if uploader.upload(metricFile, False):
                out = open(metricFile, 'w')
                out.write('[')
            # todo retry if failed?

#rp.close()
