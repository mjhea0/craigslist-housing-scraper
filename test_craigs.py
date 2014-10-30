import unittest
from craigs import CraigslistAptScraper


class CraigslistAptScraperTest(unittest.TestCase):

    def setUp(self):
        # inputs
        min_price = 1000
        max_price = 1000
        number_of_bedrooms = 3
        city = 'boulder'  # update, if necessary
        url = 'http://{}.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss'.format(city, number_of_bedrooms, max_price, min_price)
        fromaddr = "your_email@gmail.com"
        gmail_password = "dummy_email_password"
        subject = 'regarding your listing on craigslist'  # update, if necessary
        content = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'  # update, if necessary
        self.create = CraigslistAptScraper(
            min_price, max_price, number_of_bedrooms, city,
            url, fromaddr, gmail_password, subject, content)

    def test_extract_rss_link(self):
        self.assertTrue(self.create.extract_rss_link())

    def test_collect_emails(self):
        self.assertTrue(
            self.create.collect_emails(self.create.extract_rss_link()))

    def test_send_emails(self):
        pass


if __name__ == '__main__':
    unittest.main()
