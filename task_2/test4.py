__author__ = 'heocon'
import dryscrape
from threading import Thread
import logging

filename='data.xml'
arg1='MacBook'
arg2='stuxnet'
logfile='file.log'

class client():

    def __init__(self):
        self.data = []
        #self.file={}
        self.file1={}
        self.file2={}
        self.threads = []
        #define logger
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logfile,
                    filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        # define a Handler which writes INFO messages or higher to the sys.stderr


    def google(self,arg,savefile):
    #def google(self,arg):
        sess = dryscrape.Session(base_url = 'http://scholar.google.fr')
        logging.info('Visiting in google scholar')
        #print 'Visiting in google scholar'
        sess.visit('/scholar?hl=en&q='+arg)
        content= sess.xpath('//*[@class="gs_rs"]')
        if content==None:
            logging.error('Site is invalid when visiting')
            return -1
        logging.debug('Scrapping content')
        #print 'Scrapping content'
        author=sess.xpath('//*[@class="gs_a"]')
        logging.debug('Scrapping author')
        #print 'Scrapping author'
        title=sess.xpath('//*[@class="gs_rt"]')
        logging.debug('Scrapping title')
        with open(savefile,'a') as f:
            logging.info('Star writing in example.log with google search')
            f.write('<?xml version="1.0" ?>\n')
            f.write('<mydata>\n')
            for n in range(0,len(content)-1):
                logging.info('Write in each row  %d of google search' %n)
                f.write('  <row>\n')
                a=self.namespace={"title":title[n].text(),"author":author[n].text(),"content":content[n].text()}
                #self.file1[n] = a
                if a['title']==None:
                    logging.error('Site is invalid in google search')
                    return -1
                else:
                    for key1 in a.keys():
                        if key1==None:
                            logging.error("Site is invalid")
                            exit()
                        b='    <'+str(key1)+'>'+str(a[key1])+'</'+str(key1)+'>\n'
                        f.write(b)
                f.write('  </row>\n')
            f.write('</mydata>\n')
    def amazon(self,arg,savefile):
    #def amazon(self,arg):
        sess=dryscrape.Session(base_url = 'http://www.amazon.com')
        logging.info('Visiting in amazon')
        #print 'Visiting in amazon'
        sess.visit('/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+arg)

        # save in the dictionary form
        with open(savefile,'a') as f:
            logging.info('Writing in example.log with amazon search')
            f.write('<?xml version="1.0" ?>\n')
            f.write('<mydata>\n')
            for i in range(0,15):
                f.write('  <row>\n')
                a=self.search_amazon(i,sess)
                logging.info('Write in each row  %d of amazon search' %i)
                #self.file1[i] = a
                if a['name']==None:
                    logging.error("Site is invalid in amazon search")
                    return -1
                else:
                    for key in a.keys():
                        b='    <'+str(key)+'>'+str(a[key])+'</'+str(key)+'>\n'
                        f.write(b)
                f.write('  </row>\n')
            f.write('</mydata>\n')


    def search_amazon(self,i,sess):
        name='//li[@id="result_'+str(i)+'\"]'
        nodes=sess.xpath(name)
        logging.debug('Scrapping item')
        #print 'Scraping item'
        ref=None
        name=None
        price=None
        descrip=None
        otherprice=None
        shipping=None
        star=None
        for node in nodes:
            node2=node.xpath('div/div[2][@class="a-row a-spacing-mini"]')
            if node2==None:
                logging.error('Website is invalid when visiting amazon')
                return -1
            node3=node.xpath('div/div[3][@class="a-row a-spacing-mini"]')
            node4=node.xpath('div/div[4][@class="a-row a-spacing-top-mini a-spacing-mini"]')
            node5=node.xpath('div/div[5][@class="a-row a-spacing-none"]')
            for a in node2:
                a_1=a.xpath('div/a[@href]')
                logging.debug('Scrapping title and link')
                #print 'Scrapping title and link'
                for b in a_1:
                    ref=b['href']
                    name=b['title']
                    if name==None:
                        logging.error('Name is invalid')
                        return -1
            for a in node3:
                f=a.xpath('div')
                i=len(f)
                logging.debug('Scrapping price, description, and other_price')
                #print 'Scrapping price, description, and other_price'
                a_2=a.xpath('div/a/span[@class="a-size-base a-color-price s-price a-text-bold"]')
                #if a_2==None:
                 #   logging.error('Price is invalid')
                  #  return -1
                a_3=a.xpath('div[2]/div/span[@class="a-size-small a-color-price"]')
                #if a_3==None:
                 #   logging.error('Price is invalid')
                  #  return -1
                a_4=a.xpath('div['+str(i)+']/a/span[@class="a-size-base a-color-price a-text-bold"]')
                #if a_4==None:
                 #   logging.error('Price is invalid')
                  #  return -1
                for b in a_2:
                    price=b.text()
                for c in a_3:
                    descrip=c.text()
                for d in a_4:
                    otherprice=d.text()
            for a in node4:
                logging.debug('Scrapping shipping content')
                #print 'Scrapping shipping content'
                a_5=a.xpath('div/span[@class="a-size-small a-color-secondary"]')

                for b in a_5:
                    shipping=b.text()
            for a in node5:
                logging.debug('Scrapping star of item')
                #print 'Scrapping star of item'
                star= a.text()
        # save in dictionary form
        self.namespace={'ref':ref,'name':name,'price_new':price,'price_used':otherprice,'description':descrip,'shipping':shipping,'star':star}
        return self.namespace
    #def save_file(self,filename):
    def save_file(self,filename,file):
        with open(filename,'w') as f:
            row=file
            logging.info('Save in example.log')
            #print 'Save in example.log'
            ##row = file
            #f.write('<?xml version="1.0" ?>\n')
            #f.write('<mydata>\n')
            #for i in range(0,len(row)-1):
             #   f.write('  <row>\n')
            for key in row.keys():
                if key==None:
                    logging.error('Site is invalid')
                    exit()
                a='    <'+str(key)+'>'+str(row[key])+'</'+str(key)+'>\n'
                f.write(a)
              #  f.write('  </row>\n')
            #f.write('</mydata>\n')


    def go(self):
        #self.google(arg2)
        #self.amazon(arg1)
        t1 = Thread(target=self.google,args=(arg2,filename))
        t2 = Thread(target=self.amazon,args=(arg1,filename))

        t1.start()
        t2.start()
        self.threads.append(t1)
        self.threads.append(t2)

        [t.join() for t in self.threads]
def main():
    a = client()
    a.go()

if __name__ == "__main__":
    main()





