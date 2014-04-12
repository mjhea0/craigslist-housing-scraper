import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import feedparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class CraigslistAptScraper(object):

    def __init__(self, min_price, max_price, number_of_bedrooms, city, url, fromaddr, gmail_password, subject, content):
        self.min_price = min_price
        self.max_price = max_price
        self.number_of_bedrooms = number_of_bedrooms
        self.city = city
        self.url = url
        self.fromaddr = fromaddr
        self.gmail_password = gmail_password
        self.subject = subject
        self.content = content

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
        email_addresses = list(set(email_addresses))
        if len(email_addresses) > 0:
            print "Scraped {} emails".format(count - 1)
            return list(set(email_addresses))
        else:
            print "Sorry no emails were scraped. Try widening your search criteria.\n"
            return 0

    def send_emails(self, all_emails):
        print "\nSending emails ..."
        all_emails = ['hermanmu@gmail.com', 'hermanmu@gmail.com']  # testing
        # connect to the server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        try:
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
        except smtplib.SMTPAuthenticationError:
            print "Sorry. Your Gmail email address and/or password is incorrect Please try again.\n"
            return 0

    def print_statistics(self, rss_feed_results, all_emails, emails_sent):
        print "# ---------------------- Final Stats ---------------------- #"
        print "Out of {} listings, {} emails were found and {} emails were sent.\n".format(
            len(rss_feed_results), len(all_emails), emails_sent - 1)

    if __name__ == '__main__':
        # inputs
        min_price = raw_input("Enter the minimum price: ")
        max_price = raw_input("Enter your maximum price: ")
        number_of_bedrooms = raw_input("Enter the number of bedrooms: ")
        city = 'boulder'  # update, if necessary
        url = 'http://{}.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss'.format(city, number_of_bedrooms, max_price, min_price)
        fromaddr = raw_input("Enter your gmail address (include \"@gmail.com\"): ")
        gmail_password = raw_input("Enter your gmail password: ")
        subject = 'regarding your listing on craigslist'  # update, if necessary
        content = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'  # update, if necessary

        craig = CraigslistAptScraper(min_price, max_price, number_of_bedrooms, city, url, fromaddr, gmail_password, subject, content)
        rss_results = craig.extract_rss_link()
        emails = craig.collect_emails(rss_results)
        if emails != 0:
            sent = craig.send_emails(emails)
        if sent != 0:
            craig.print_statistics(rss_results.entries, emails, sent)
