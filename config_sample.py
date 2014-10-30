min_price = 1000
max_price = 3000
number_of_bedrooms = 3
city = 'boulder'
url = 'http://{}.craigslist.org/search/hhh?bedrooms={}&catAbb=hhh&maxAsk={}&minAsk={}&s=0&format=rss'.format(
    city, number_of_bedrooms, max_price, min_price)

fromaddr = 'TEST@gmail.com'
gmail_password = 'PASSWORD'
subject = 'regarding your listing on craigslist'
content = 'Hi, I\'m looking for a place to live in the area. Would it be possible to set up a time to come by and have a look? Thanks so much!'  # update, if necessary
