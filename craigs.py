import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import feedparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class CraigslistAptScraper(object):

    def init(self):
        self.min_price = raw_input("Enter the minimum price: ")
        self.max_price = raw_input("Enter your maximum price: ")
        self.number_of_bedrooms = raw_input("Enter the number of bedrooms: ")
        self.city = 'boulder'  # update, if necessary
        self.url = 'http://{}.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss'.format(self.city, self.number_of_bedrooms, self.max_price, self.min_price)
        self.fromaddr = raw_input("Enter your gmail address (include \"@gmail.com\"): ")
        self.gmail_password = raw_input("Enter your gmail password: ")
        self.subject = 'regarding your listing on craigslist'  # update, if necessary
        self.content = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'  # update, if necessary

    def extract_rss_link(self):
        os.system(['clear', 'cls'][os.name == 'nt'])
        print "Searching craigslist ..."
        d = feedparser.parse(self.url)
        print "Found {} listings.".format(len(d.entries))
        return d

    def collect_emails(self, rss_feed_results):
        print "\nGrabbing emails ..."
        email_addresses = []
        count = 1
        for listing in rss_feed_results.entries:
            driver = webdriver.PhantomJS()
            driver.get(listing.link)
            try:
                driver.find_element_by_class_name("reply_button").click()
                # driver.implicitly_wait(10)
                try:
                    # wait until selector is visible; throw exception if not visible after 10 seconds
                    element = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_element_by_class_name("reply_options")
                    )
                except TimeoutException:
                    print "timeout"
                element = driver.find_element_by_xpath('//*[@class="reply_options"]/ul[4]/li/input')
                mailto = element.get_attribute('value')
                email_addresses.append(str(mailto))
                print "Scraped email # {}".format(count)
                count += 1
            except NoSuchElementException:
                pass
            driver.quit
        # remove duplicate emails
        print "Scraped {} emails".format(count - 1)
        return list(set(email_addresses))

    def send_emails(self, all_emails):
        print "\nSending emails ..."
        all_emails = ['hermanmu@gmail.com', 'hermanmu@gmail.com']
        # connect to the server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.fromaddr, self.gmail_password)
        count = 1
        for toaddr in all_emails:
            msg = MIMEMultipart()
            msg['From'] = self.fromaddr
            msg['To'] = toaddr
            msg['Subject'] = self.subject
            msg.attach(MIMEText(self.content))
            server.sendmail(self.fromaddr, toaddr, msg.as_string())
            print "Sent email # {}".format(count)
            count += 1
        server.quit()
        print "\nDone! You sent {} emails!\n".format(count - 1)
        return count

    def print_statistics(self, rss_feed_results, all_emails, emails_sent):
        print "# ---------------------- Final Stats ---------------------- #"
        print "Out of {} listings, {} emails were found and {} emails were sent.\n".format(
            len(rss_feed_results), len(all_emails) - 1, emails_sent - 1)


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    craig.init()
    rss_results = craig.extract_rss_link()
    emails = craig.collect_emails(rss_results)
    sent = craig.send_emails(emails)
    craig.print_statistics(rss_results.entries, emails, sent)
