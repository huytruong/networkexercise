__author__ = 'hrua'

import task_1.Message as message
import task_1.CODE as CODE
import datetime
import pickle

rawFile ="../../database/randomfile"
xmlFile ="../../database/xmlfile"


usr=''
pwd=''

def checkCommand(data):
    global usr
    m= message.Message()
    m.parser(data)
    cmd = m.type
    print (pickle.loads(m.payload))
    if cmd == CODE.PUSHR:
        if not authority(m.id.strip("\n")):
            return CODE.ASK_LOGIN
        '''
            imlement store file
        '''
        save_raw(m.payload)
        return CODE.STORE_OK
    
    elif cmd == CODE.PUSHX:
        if authority(not m.id.strip("\n")):
            return CODE.ASK_LOGIN
        '''
            imlement store file
        '''
        save_xlm(str(pickle.loads(m.payload)))
        return CODE.STORE_OK
    
    elif cmd == CODE.USER:
        '''
            send back request for pass
        '''

        usr = m.payload.strip("\n")
        return CODE.ASK_PWD

    elif cmd == CODE.PASS:
        '''
            send back refuse or sessionid
        '''
        pwd = m.payload.strip("\n")
        return authen(usr,pwd)

    return CODE.UNKNOWN




def authen(user,p):
    '''
    check usrname password
    :return:True/False
    '''
    global usr
    if usr in CODE.etc_pwd:
        if CODE.etc_pwd[user] == p:
            return CODE.SESSION
        user=0
        return CODE.LOGIN_FAIL
    user=0
    return CODE.LOGIN_FAIL

def authority(s):
    if s==CODE.SESSION:
        return True
    return False


def save_raw(payload):
    f = open(rawFile, "a")
    deliminate = "\n\n+++++++"+str(datetime.datetime.now()) +"++++++\n"
    payload = deliminate+payload
    f.write(payload)
    f.close()

def save_xlm(payload):
    f = open(xmlFile, "a")
    f.write(payload+"\n")
    f.close()

    '''
    tmp= {"rank":payload[0], "team":payload[0] ,"played":payload[0],"wins":payload[0],"draws":payload[0],"losts":payload[0],
          "goal-for":payload[0],"goal-against":payload[0],"goal-different":payload[0],"points":payload[0]}
    f = open(xmlFile,'w')

    f.write('<?xml version="1.0" ?>\n')
    f.write('<livescore>\n')
    for i in range(0,len(row)-1):
        f.write('  <row>\n')
        for key in row[i].keys():
                a='    <'+str(key)+'>'+str(row[i][key])+'</'+str(key)+'>\n'
                f.write(a)
            f.write('  </row>\n')
        f.write('</livescore>\n')
    '''

