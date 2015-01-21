__author__ = 'hrua'

import time,threading
import clientsocket
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
        r = clientsocket.getContent1(self.link)

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


#print collectData()


#=======================

import argparse
import sys
import dryscrape
from collections import namedtuple
namespace = namedtuple("Dir", ["name", "value"])


class clientScrape:
    def __init__(self):
        self.data = []
        self.file={}
        parser = argparse.ArgumentParser(description='Processing key words',usage='-h -a -g')
        parser.add_argument('-a', help='Search in amazon website')
        parser.add_argument('-g', help='Search in google scholar')
        self.args = parser.parse_args(sys.argv[1:3])

    def google(self,arg):
        sess = dryscrape.Session(base_url = 'http://scholar.google.fr')
        print "Visiting in..."
        sess.visit('/scholar?hl=en&q='+arg)
        content= sess.xpath('//*[@class="gs_rs"]')
        author=sess.xpath('//*[@class="gs_a"]')
        title=sess.xpath('//*[@class="gs_rt"]')
        for i in range(0,len(content)-1):
            a=self.namespace={"title":title[i].text(),"author":author[i].text(),"content":content[i].text()}
            self.file[i]=a

    def amazon(self,arg):
        sess=dryscrape.Session(base_url = 'http://www.amazon.com')
        print "Visiting in..."
        sess.visit('/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+arg)
        # save in the dictionary form
        for i in range(0,10):
            a=self.search_amazon(i,sess)
            self.file[i]=a

    def search_amazon(self,i,sess):
        name='//li[@id="result_'+str(i)+'\"]'
        nodes=sess.xpath(name)
        ref=None
        name=None
        price=None
        descrip=None
        otherprice=None
        shipping=None
        star=None
        for node in nodes:
            node2=node.xpath('div/div[2][@class="a-row a-spacing-mini"]')
            node3=node.xpath('div/div[3][@class="a-row a-spacing-mini"]')
            node4=node.xpath('div/div[4][@class="a-row a-spacing-top-mini a-spacing-mini"]')
            node5=node.xpath('div/div[5][@class="a-row a-spacing-none"]')
            for a in node2:
                a_1=a.xpath('div/a[@href]')
                for b in a_1:
                    ref=b['href']
                    name=b['title']
            for a in node3:
                f=a.xpath('div')
                i=len(f)
                a_2=a.xpath('div/a/span[@class="a-size-base a-color-price s-price a-text-bold"]')
                a_3=a.xpath('div[2]/div/span[@class="a-size-small a-color-price"]')
                a_4=a.xpath('div['+str(i)+']/a/span[@class="a-size-base a-color-price a-text-bold"]')
                for b in a_2:
                    price=b.text()
                for c in a_3:
                    descrip=c.text()
                for d in a_4:
                    otherprice=d.text()
            for a in node4:
                a_5=a.xpath('div/span[@class="a-size-small a-color-secondary"]')
                for b in a_5:
                    shipping=b.text()
            for a in node5:
                star= a.text()
        # save in dictionary form
        self.namespace={'ref':ref,'name':name,'price_new':price,'price_used':otherprice,'description':descrip,'shipping':shipping,'star':star}
        return self.namespace

a=clientScrape()
amazon='../database/amazon.xml'
google='../database/googe.xml'
if a.args.a:
    arg=a.args.a
    a.amazon(arg)
    a.save_file(amazon)
else:
    arg=a.args.g
    a.google(arg)
    a.save_file(google)
