__author__ = 'hrua'

import threading
import client
#import multithreadClient
import task_1.Message
server = "localhost"
port = 9191

class connectDBThread(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg

    def run(self):
        print "opening a connection to database ...\n"
        s, target,remote_ip = client.reachTarget(server, port)
        message = self.msg
        print message
        s.send(message)
        ans=s.recv(1024)
        print "ANSWWER FORM SERVR :" +ans
        s.close()


#result = multithreadClient.collectData()
#result =["truong","quang","huy"]
for i in result:
e = task_1.Message.Message("PUSHF", mid="1111", mpayload="hjijsdiajfyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyG")
print e
m = connectDBThread(str(e))
m.start()
