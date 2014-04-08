import feedparser
import smtplib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CraigslistAptScraper(object):

    def init(self):
        self.min_price = 1000
        self.max_price = 3000
        self.number_of_bedrooms = 2
        # self.gmail_address = raw_input("Enter your gmail address: ")
        # self.gmail_password = raw_input("Enter your gmail address password: ")
        self.url = 'http://boulder.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss'.format(self.number_of_bedrooms, self.max_price, self.min_price)
        self.subject = 'regarding your listing on craigslist'
        self.message = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'

    def extract_rss_link(self):
        print "searching ..."
        d = feedparser.parse(self.url)
        return d

    def collect_emails(self, rss_feed_results):
        print "grabbing emails ..."
        email_addresses = []
        count = 1
        for listing in rss_feed_results.entries:
            driver = webdriver.PhantomJS()
            driver.get(listing.link)
            try:
                driver.find_element_by_class_name("reply_button").click()
                element = driver.find_element_by_xpath('//*[@class="reply_options"]/ul[4]/li/input')
                mailto = element.get_attribute('value')
                email_addresses.append(mailto)
                print "added {} email(s)".format(count)
                count += 1
            except NoSuchElementException:
                pass
            driver.quit
        print list(set(email_addresses))
        return email_addresses

    def send_emails(self, all_emails):
        # remove duplicate emails
        print list(set(email_addresses)) 
  
        print "sending emails ..."
        server = smtplib.SMTP('smtp.gmail.com:587')  
        server.starttls()  
        server.login(self.gmail_address, self.gmail_password)
        count = 1 
        for address in email_addresses: 
            server.sendmail(self.gmail_address, address, self.subject, self.message)
            print "added {} email(s)".format(count)
            count += 1  
        server.quit()  


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    craig.init()
    rss_results = craig.extract_rss_link()
    emails = craig.collect_emails(rss_results)
    # craig.send_emails(emails)
