__author__ = 'heocon'
import argparse
import sys
import dryscrape
class client:
    def __init__(self):
        self.data = []
        parser = argparse.ArgumentParser(description='Processing key words',usage='-h -a -s')
        parser.add_argument('-a', help='Search in amazon website')
        parser.add_argument('-s', help='Search in google scholar')
        self.args = vars(parser.parse_args(sys.argv[1:3]))
    def google(self,arg):
        sess = dryscrape.Session(base_url = 'http://scholar.google.fr')
        print "Visiting in..."
        sess.visit('/scholar?hl=en&q='+arg)
        content= sess.xpath('//*[@class="gs_rs"]')
        author=sess.xpath('//*[@class="gs_a"]')
        title=sess.xpath('//*[@class="gs_rt"]')
        self.file=[]
#print len(content)
        for i in range(0,len(content)-1):
            self.file.append(title[i].text() + '||' + author[i].text() + '||' + content[i].text())
        print self.file[0]
        return self.file
    def amazon(self,arg):
        sess=dryscrape.Session(base_url = 'http://www.amazon.com')
        print "Visiting in..."
        sess.visit('/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+arg)

        #sess.render('test.png')
        #article=sess.xpath('//[@class=a]')
        #for link in article:
         #  print link['class']
        nodes=sess.xpath('//li[@id="result_0"]')
        for node in nodes:
            link=node.xpath('div/div/div/div/a[@href]')
            price=node.xpath('//span[@class="a-size-base a-color-price s-price a-text-bold"]')
            ship=node.xpath('//span[@class="a-size-small a-color-secondary"]')
            vote=node.xpath('//a[@class="a-size-small a-link-normal a-text-normal"]')
            descrip=node.xpath('//span[@class="a-size-small a-color-price"]')
            for a in link:
                print a['href']
            for b in price:
                print b.text()
            for c in ship:
                print c.text()
            for d in vote:
                print d.text()
            for e in descrip:
                print e.text()
        #print nodes1[0].text()
        #name=[]
        #print arg
        #for link in article:
         #   if arg in link['title']:
          #      name.append(link['title'])

            #if any("MacBook" in s for s in link['title']):
        #name.append(link['title'])
        #print name
        #return self.file
        #name=
        #price=
        #offer=
        #novote=


a=client()
arg=sys.argv[2]
#print a.args
#print arg
a.amazon(arg)

#result_0 > div:nth-child(1)

#<Node #/html/body/div[@id='a-page']/div[@id='main']/div[@id='searchTemplate']/div[@id='rightContainerATF']/div[@id='rightResultsATF']/div[@id='resultsCol']/div[@id='centerMinus']/div[@id='atfResults']/ul[@id='s-results-list-atf']/li[@id='result_0']/div>

#title="Apple MacBook Air MD711LL/B 11.6-Inch Laptop (NEWEST VERSION)" href="http://www.amazon.com/Apple-MacBook-MD711LL-11-6-Inch-VERSION/dp/B00746YZS6/ref=sr_1_1?s=pc&amp;ie=UTF8&amp;qid=1421589716&amp;sr=1-1&amp;keywords=macbook"



