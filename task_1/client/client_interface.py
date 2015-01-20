__author__ = 'hrua'
import sys

i=1
while i in range(1,4):
    print "1. Login\n"
    print "2. Scrap and save to a file on server\n"
    print "3. Multi scrap from Google Scholar and save to database xml\n"
    print "0. Exit"

    i = raw_input("Choose option: --> ")
    if i.isdigit():
        i = int(i)
        if i==1:
            print str(1)
        elif i ==2:
            print str(2)
        elif i ==3:
            print str(3)
        elif i == 0:
            break
