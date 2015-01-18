__author__ = 'heocon'
import dryscrape

sess = dryscrape.Session(base_url = 'http://scholar.google.fr')

print "Visiting in..."
sess.visit('/scholar?hl=en&q=stuxnet')
sess.render('google1.png')
content= sess.xpath('//*[@class="gs_rs"]')
author=sess.xpath('//*[@class="gs_a"]')
title=sess.xpath('//*[@class="gs_rt"]')
file=[]
#print len(content)
for i in range(0,len(content)-1):
    file.append(title[i].text() + '||' + author[i].text() + '||' + content[i].text())





