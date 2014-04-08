import feedparser
import smtplib
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
        self.gmail_address = raw_input("Enter your gmail address: ")
        self.gmail_password = raw_input("Enter your gmail password: ")
        self.subject = 'regarding your listing on craigslist'  # update, if necessary
        self.message = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'  # update, if necessary

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
        print list(set(all_emails))
        all_emails = ['hermanmu@gmail.com']
        print "sending emails ..."
        # fire up gmail
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(self.gmail_address, self.gmail_password)
        count = 1
        for address in all_emails:
            server.sendmail(self.gmail_address, address, self.subject, self.message)
            print "added {} email(s)".format(count)
            count += 1
        server.quit()


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    craig.init()
    rss_results = craig.extract_rss_link()
    emails = craig.collect_emails(rss_results)
    craig.send_emails(emails)
