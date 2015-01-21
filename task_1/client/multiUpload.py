__author__ = 'hrua'

import threading
import clientsocket
import sys
import task_1.Message
import pickle
server = "localhost"
port = 9191

code_lock =threading.Lock()
code=0

class connectDBThread(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg

    def run(self):
        global code
        s=''
        taget=''
        remote_ip =''
        try:
            print "(%s) opening a connection to database ...\n"%(self.getName())
            s, target,remote_ip = clientsocket.reachTarget(server, port)
        except:
            print "!!!! Cannot reach the server at moment"
            sys.exit()

        message = self.msg
        print "(%s) send message --> %s\n"%(self.getName(),message)
        try:
            s.send(message)
            ans=s.recv(1024)
            code_lock.acquire()
            code=ans
            code_lock.release()

            print "(%s) received answer -->%s\n"%(self.getName(),ans)
            s.close()



        except:
            print "!!!! Cannot send data "



#result = multithreadClient.collectData()
#result =["truong","quang","huy"]

def send(command,id,data):
    '''
    send data to server , support multithread
    :param command:
    :param id:
    :param data:
    :return:
    '''
    if isinstance(data,list):
        running=[]
        for obj in data:
            e = task_1.Message.Message(command,id, pickle.dumps(obj))
            m = connectDBThread(str(e))
            m.start()
            running.append(m)

        [m.join() for m in running]


    elif isinstance(data,str):
        e = task_1.Message.Message(command,id, data)
        m = connectDBThread(str(e))
        m.start()

    return code


a,x = clientsocket.getContent("/soccer/england/premier-league/")
#print x
print send("PUSHX",1111,x)
