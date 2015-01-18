__author__ = 'heocon'

import time
import dryscrape

#==========================================
# Setup
#==========================================

email    = 'an.dang.ict@jvn.edu.vn'
password = 'Heocon456%'

# set up a web scraping session
sess = dryscrape.Session(base_url = 'https://mail.google.com/')

# we don't need images
sess.set_attribute('auto_load_images', False)

# if we wanted, we could also configure a proxy server to use,
# so we can for example use Fiddler to monitor the requests
# performed by this script
#sess.set_proxy('localhost', 8888)

#==========================================
# GMail send a mail to self
#==========================================

# visit homepage and log in
print "Logging in..."
sess.visit('/')

email_field    = sess.at_css('#Email')
#print type(email_field)
password_field = sess.at_css('#Passwd')
email_field.set(email)
password_field.set(password)

email_field.form().submit()


# find the COMPOSE button and click it
print "Sending a mail..."
#compose = sess.at_xpath('//*[contains(text(), "COMPOSE")]')
compose=sess.at_xpath('//div[text()="COMPOSE"]')
#print compoe
compose.click()


# compose the mail
to      = sess.at_xpath('//*[@name="to"]', timeout=10)
subject = sess.at_xpath('//*[@name="subjectbox"]')
body    = sess.at_xpath('//div[@role="textbox"]')




to.set(email)
subject.set("Note to self")
body.set("Remember to try dryscrape!")

# send the mail

# seems like we need to wait a bit before clicking...
# Blame Google for this ;)
time.sleep(3)
send = sess.at_xpath('//*[normalize-space(text()) = "Send"]')
send.click()

# open the mail
print "Reading the mail..."
mail = sess.at_xpath('//*[normalize-space(text()) = "Note to self"]',
                     timeout=10)
mail.click()

# sleep a bit to leave the mail a chance to open.
# This is ugly, it would be better to find something
# on the resulting page that we can wait for
time.sleep(3)

# save a screenshot of the web page
print "Writing screenshot to 'gmail.png'"
sess.render('gmail.png')


