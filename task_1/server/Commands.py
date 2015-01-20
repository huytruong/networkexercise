__author__ = 'hrua'

import task_1.Message as message
import task_1.code as CODE

writtenFile ="../../database/randomfile"
dbFile ="../../database/dbfile"


user=''
pwd=''

def checkCommand(data):
    m= message.Message()
    m.parser(data)
    cmd = m.type

    print m.id

    if cmd == CODE.PUSHF:
        if authority(not m.id.strip("\n")):
            return CODE.ASK_LOGIN
        '''
            imlement store file
        '''
        save_file(m.payload)
        return CODE.STORE_OK
    
    elif cmd == CODE.PUSHO:
        if authority(not m.id.strip("\n")):
            return CODE.ASK_LOGIN
        '''
            imlement store file
        '''
        print "LUU FILE THANH CONG" +str(CODE.STORE_OK)
        return CODE.STORE_OK
    
    elif cmd == CODE.USER:
        '''
            send back request for pass
        '''
        usr= m.payload.strip("\n")
        return CODE.ASK_PASS

    elif cmd == CODE.PASS:
        '''
            send back refuse or sessionid
        '''
        pwd=m.payload.strip("\n")
        return authen(user,pwd)

    return CODE.UNKNOWN




def authen(usr,p):
    '''
    check usrname password
    :return:True/False
    '''

    if usr in CODE.etc_pwd:
        if CODE.etc_pwd[usr] == p:
            return CODE.SESSION
        return CODE.LOGIN_FAIL
    return CODE.LOGIN_FAIL

def authority(s):
    if s==CODE.SESSION:
        return True
    return False


def save_file(payload):
    f = open(writtenFile, "a")
    f.write(payload)
    f.close()
