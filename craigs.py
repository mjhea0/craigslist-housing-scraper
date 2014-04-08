import feedparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CraigslistAptScraper(object):

    def init(self):
        self.min_price = 1000
        self.max_price = 3000
        self.number_of_bedrooms = 2
        # self.gmail_address = raw_input("Enter your gmail address: ")
        # self.gmail_password = raw_input("Enter your gmail address password: ")
        self.url = "http://boulder.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss".format(self.number_of_bedrooms, self.max_price, self.min_price)

    def extract_rss_link(self):
        # print self.url
        d = feedparser.parse(self.url)
        # print "\nTotal Listings: {}\n".format(len(d))
        # for post in d.entries:
        #     print "Title: {}\nLink: {}\n".format(post.title, post.link)
        return d

    def collect_emails(self, rss_feed_results):
        email_addresses = []
        for listing in rss_feed_results.entries:
            driver = webdriver.PhantomJS()
            driver.get(listing.link)
            try:
                driver.find_element_by_class_name("reply_button").click()
                element = driver.find_element_by_xpath('//*[@class="reply_options"]/ul[4]/li/input')
                mailto = element.get_attribute('value')
                email_addresses.append(mailto)
            except NoSuchElementException:
                pass
            driver.quit
        # remove duplicate emails
        return list(set(email_addresses))

    def send_emails(self, all_emails):
        print all_emails


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    craig.init()
    rss_results = craig.extract_rss_link()
    emails = craig.collect_emails(rss_results)
    craig.send_emails(emails)
