#!/usr/bin/python
import time


def reader(uploader, pipe):
    metricFile = "./pendingMetrics.json"
    out = open(metricFile, 'w')
    out.write('[')

    rp = open(pipe, 'r')  # Blocks here until the first message is sent

    metricCount = 0
    done = False
    while not done:
        response = rp.readline()
        if not response:
            time.sleep(0.05)
        else:
            metric = response.split(' ')

            # todo use Object to encode json
            if metricCount > 0:
                out.write(',')
            out.write('{')
            out.write('"name": "%s",' % metric[0])
            out.write('"timestamp": %s,' % int(round(time.time() * 1000)))
            out.write('"value": %s,' % metric[1])

            out.write('"tags":{')
            tagCount = 0
            for tagString in metric[2:]:
                if tagCount > 0:
                    out.write(',')
                tag = tagString.split('=')
                out.write('"%s": "%s"' % (tag[0], tag[1]))
                tagCount +=1
            out.write('}')

            out.write('}')

            out.flush()
            metricCount += 1

        if metricCount > 9:
            metricCount = 0
            out.write(']')
            out.close()
            if uploader.upload(metricFile):
                out = open(metricFile, 'w')
                out.write('[')
            # todo retry if failed?

#rp.close()
