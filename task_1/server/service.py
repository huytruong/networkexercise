__author__ = 'hrua'


import socket
import threading
import Commands
import task_1.Message as m
port = 9191
host = "127.0.0.1"

#maybe relate to readfile
handler_request_lock = threading.Lock()

class ServerSocket(threading.Thread):
    def __init__(self, conn, addinfo):
        threading.Thread.__init__(self)
        self.conn =conn
        self.addr =addinfo
        self.daemon=True

    def run(self):
        msg=''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = msg+data
            if (isEOF(repr(msg))):
                break
        handler_request_lock.acquire()
        re = Commands.checkCommand(msg)
        handler_request_lock.release()
        conn.send(str(re))

def isEOF(data):
    msg= m.Message()
    msg.parser(data)

    if msg.len != len(msg.payload):
        return False
    return True

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind((host,port))
srv.listen(5)
print ("www")

while True:
    print ("server is waiting\n ")
    conn, addr = srv.accept()

    ServerSocket(conn, addr).start()
    print ("There is one imcomming data....\n")


