import socket
import sys
import re
from task_1.Article import  Article


def reachTarget(target = "www.livescore.com",port = 80):
    '''

    :param target: main link of site needed to crawler //remove http://
    :param port: port of site . default: 80
    :return: socket,hostname, ip
    '''
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    #print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( target )
    except socket.gaierror:
        #could not resolve
        print 'Hostname could not be resolved. Exiting'
        sys.exit()
    #print 'Ip address of ' + target + ' is ' + remote_ip

    #Connect to remote server
    s.connect((target , port))
    return s, target,remote_ip




def getContent(sublink):
    '''
    prepare the request and send to server.
    :param sublink ; format /abc/xhz
    :return: string -- content of page.
    '''

    s,target,remote_ip = reachTarget()
    #print 'Socket Connected to ' + target + ' on ip ' + remote_ip

    #Send some data to remote server

    message="GET "+sublink+" HTTP/1.1\r\n" \
            "Host: "+target+"\r\n\r\n"
    print message
    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
    print 'Message send successfully'
    data=''
    i=0
    while True:
        reply = s.recv(1024)
        #print reply

        data= data+str(reply)
        if "</html>" in reply:
            s.close()
            break

    return doParser(data)

'''
def doParserGoogleScholar(content):

    result = []
    parsed_html = BeautifulSoup.BeautifulSoup(content)

    articles = parsed_html.findAll('div', { "class" : "gs_r" })

    for art in articles:
        art_html = BeautifulSoup.BeautifulSoup(str(art))

        if art_html.find("div", {'class':"gs_a"}):
            author = art_html.find("div", {'class':"gs_a"}).contents
        if art_html.find("div", {'class':"gs_rs"}):
            desc = art_html.find("div", {'class':"gs_rs"}).contents
        if art_html.find("h3", {'class':"gs_rt"}):
            tit = art_html.find("h3", {'class':"gs_rt"}).contents
            tit_html = BeautifulSoup.BeautifulSoup(str(tit))
            a = tit_html.findAll("a")
            if len(a)!=0:
                link = a[0]['href']
                tit= a[0].contents

        print "title: --> "+str(tit)
        print "author: --> " +str(author)
        print "desc : --> "+ str(desc)
        print "link --> "+str(link)

        ar = Article(str(tit),str(author),str(link),str(desc))
        result.append(ar)

    return result
'''

def doParser(data):
    '''
    :param data:
    :return:
    '''
    rawtable=''
    row_objects=[]
    t= re.search('<table class="league-wc table mtn">(.*)</table>', data)

    if t:
        rawtable =t.group(0)

        #get rows
        r  = re.findall("<tr[^>]+>(.*?)<\/tr>",rawtable)
        #skip column title
        for row in r[1:]:
            #print row
            col = re.findall("<td[^>]*>(.*?)<\/td>",row)

            col[1] = re.sub('<div class="num">(.*)</div>', r"\1",col[1]).strip()
            #remove the first useless column
            col.pop(0)
            row_objects.append(col)
    return rawtable,row_objects

a1 = Article("111","111","111","111")
a2 = Article("222","222","222","222")
a3 = Article("333","333","333","333")
a4 = Article("4444","4444","4444","4444")
def getContent1(LINKS):
    return [a1,a2,a3,a4]


#content = getContent("/soccer/england/premier-league/")
#content = getContent("/scholar?start=10&q=stuxnet")

