__author__ = 'hrua'

import time,threading
import client
LINKS =[
    "/scholar?q=stuxnet",
    "/scholar?start=10&q=stuxnet",
    "/scholar?start=20&q=stuxnet"
]
result_lock = threading.Lock()
result =[]

class MultiScrapy(threading.Thread):
    def __init__(self,link):
        threading.Thread.__init__(self)
        self.link = link

    def run(self, ):
        global result
        r = client.getContent(self.link)

        print "Start process" + self.getName()

        result_lock.acquire()
        #get content for each link
        result.extend(r)

        result_lock.release()

        print "Complete process" + self.getName();

running=[]

for i in LINKS:
    m=MultiScrapy(i)
    m.start()
    running.append(m)

[ m.join() for m in running]

print len(result)