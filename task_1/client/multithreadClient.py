__author__ = 'hrua'

import time,threading
import client
LINKS =[
    "/scholar?q=bigdata",
    "/scholar?start=10&q=bigdata",
    "/scholar?start=20&q=bigdata"
]
result_lock = threading.Lock()
result =[]

class ThreadScrapy(threading.Thread):
    def __init__(self,link):
        threading.Thread.__init__(self)
        self.link = link

    def run(self, ):
        global result
        r = client.getContent1(self.link)

        print "Start process" + self.getName()

        result_lock.acquire()
        #get content for each link
        result.extend(r)

        result_lock.release()

        print "Complete process" + self.getName();


def collectThreads(LINKS):
    running=[]

    for i in LINKS:
        m=ThreadScrapy(i)
        m.start()
        running.append(m)

    [ m.join() for m in running]


def collectData():
    collectThreads(LINKS)
    return result


print collectData()