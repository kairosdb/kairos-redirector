#!/usr/bin/python
import time
import threading


class Reader(threading.Thread):
    def __init__(self, uploader, pipe):
        self.uploader = uploader
        self.pipe = pipe
        self.done = False

        threading.Thread.__init__(self, target = self.reader)
        self.start()

    def stop(self):
        self.done = True


    def reader(self):
        metricFile = "./pendingMetrics.json"
        out = open(metricFile, 'w')
        out.write('[')

        rp = open(self.pipe, 'r')  # Blocks here until the first message is sent

        metricCount = 0
        startTime = time.time()
        while not self.done:
            # print "Running"
            response = rp.readline()
            if not response:
                time.sleep(0.05)
            else:
                metric = response.strip().split(' ')

                if (len(metric) < 3):
                    print 'Bad metric ' + response
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
                    tagCount += 1
                out.write('}')

                out.write('}')

                out.flush()
                metricCount += 1

            if time.time() > (startTime + 10) and metricCount > 0:
                print "sending metric"
                metricCount = 0
                out.write(']')
                out.close()
                if self.uploader.upload(metricFile, False):
                    out = open(metricFile, 'w')
                    out.write('[')
                    # todo retry if failed?
                startTime = time.time()
