import os
import smtplib
import feedparser
import sqlite3
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import *


class CraigslistAptScraper(object):

    def __init__(self, min_price, max_price,
                 number_of_bedrooms, city, url,
                 fromaddr, gmail_password, subject, content):
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
        listings = feedparser.parse(self.url)
        print "Found {} listings.".format(len(listings.entries))
        return listings

    def collect_emails(self, rss_feed_results):
        print "\nGrabbing emails ..."
        email_addresses = []
        count = 1
        for listing in rss_feed_results.entries:
            driver = webdriver.PhantomJS()
            driver.get(str(listing.dc_source))
            try:
                driver.find_element_by_class_name("reply_button").click()
                # driver.implicitly_wait(10)
                try:
                    # wait until selector is visible;
                    # throw exception if not visible after 10 seconds
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.CLASS_NAME, "reply_options"))

                    )
                except TimeoutException:
                    print "timeout"
                element = driver.find_element_by_class_name("mailto")
                # element = driver.find_element_by_xpath(
                #     '//*[@class="reply_options"]/ul[4]/li/input')
                # mailto = element.get_attribute('value')
                email_addresses.append(str(element.text))
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
            print "No emails were scraped. Try widening your search criteria.\n"
            return 0

    def add_to_database(self, all_emails):
        new_emails = []
        # create database and table (if necessary)
        con = sqlite3.connect('emails.db')
        with con:
            cur = con.cursor()
            try:
                cur.execute(
                    "CREATE TABLE emails(id INTEGER PRIMARY KEY, email TEXT)")
            except sqlite3.OperationalError:
                pass
            # loop through scrapped emails
            for email in all_emails:
                cur.execute("SELECT * FROM emails where email = ?", (email,))
                check = cur.fetchone()
                # if email is not in db, add it to the db and to the list
                if check is None:
                    cur.execute("INSERT INTO emails(email) VALUES (?)",
                                (email,))
                    new_emails.append(email)
            return new_emails

    def send_emails(self, new_emails):
        print "\nSending emails ..."
        # connect to the server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        try:
            server.login(self.fromaddr, self.gmail_password)
            count = 1
            for toaddr in new_emails:
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
            print "The email address and/or password is incorrect. try again.\n"
            return 0

    def print_statistics(self, rss_feed_results, all_emails, emails_sent):
        print "# ---------------------- Final Stats ---------------------- #"
        print "Out of {} listings...".format(len(rss_feed_results))
        print "...{} emails were found and {} emails were sent.\n".format(
            len(all_emails), emails_sent - 1)

if __name__ == '__main__':

    craig = CraigslistAptScraper(
        min_price, max_price, number_of_bedrooms,
        city, url, fromaddr, gmail_password, subject, content)
    rss_results = craig.extract_rss_link()
    all_emails = craig.collect_emails(rss_results)
    if all_emails:
        new_emails = craig.add_to_database(all_emails)
        if new_emails != 0:
            sent = craig.send_emails(new_emails)
            if sent != 0:
                craig.print_statistics(rss_results.entries, all_emails, sent)
