import feedparser
import requests


class CraigslistAptScraper(object):

    def init(self):
        self.min_price = 1000
        self.max_price = 3000
        self.number_of_bedrooms = 2
        # self.gmail_address = raw_input("Enter your gmail address: ")
        # self.gmail_password = raw_input("Enter your gmail address password: ")
        self.url = "http://boulder.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss".format(self.number_of_bedrooms, self.max_price, self.min_price)

    def extract_rss_link(self):
        print self.url
        d = feedparser.parse(self.url)
        print "\nTotal Listings: {}\n".format(len(d))
        for post in d.entries:
            print "Title: {}\nLink: {}\n".format(post.title, post.link)

    def collect_emails(self):
        r = requests.get('https://api.github.com/user')
        print r.status

    def send_emails(self):
        pass


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    craig.init()
    craig.extract_rss_link()
