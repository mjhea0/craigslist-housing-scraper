

class CraigslistAptScraper(object):

    def init(self):
        self.min_price = 1000
        self.max_price = 3000
        self.number_of_bedrooms = 2
        self.gmail_address = raw_input("Enter your gmail address: ")
        self.gmail_password = raw_input("Enter your gmail address password: ")

    def gather_info(self):
        pass

    def extract_rss_link(self):
        pass

    def collect_emails(self):
        pass

    def send_emails(self):
        pass


if __name__ == '__main__':
    craig = CraigslistAptScraper()
    test = craig.init()
