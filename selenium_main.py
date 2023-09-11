from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from helpers import *
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

browser = webdriver.Firefox()
# This is my profile containing all read and unread books
url = r'https://www.goodreads.com/review/list/142380450-mauricio-pujol?utf8=%E2%9C%93&shelf=%23ALL%23&per_page=infinite'
browser.get(url)
time.sleep(2)

scroll_pause_seconds = 1
# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(scroll_pause_seconds)
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
html_tr = soup.find_all("tr")
df_my_books = pd.DataFrame({'title': pd.Series(dtype='str'),  # This defines the structure for the dataframe to store scraped data
                            'author': pd.Series(dtype='str'),
                            'pages': pd.Series(dtype='int'),
                            'avg_rating': pd.Series(dtype='float'),
                            'num_ratings': pd.Series(dtype='int'),
                            'date_pub': pd.Series(dtype='str'),
                            'rating': pd.Series(dtype='int'),
                            'cover_link': pd.Series(dtype='str')
                            # 'c': pd.Series(dtype='float')
                            })
for i in range(0, len(html_tr)):
    try:
        df_my_books.loc[len(df_my_books.index)] = [
            html_tr[i].find('td', {'class': 'field title'}
                            ).a.text.strip(),  # Extract book title
            html_tr[i].find('td', {'class': 'field author'}
                            ).a.text.strip(),  # Extract book author
            # Extract book number of pages
            get_number_of_pages(html_tr[i].find('td',
                                                {'class': 'field num_pages'}).text),
            # Extract average rating
            float(re.search(r'[\d+\.\d+]+', html_tr[i].find('td',
                  {'class': 'field avg_rating'}).text).group()),
            int(''.join([n for n in html_tr[i].find('td', {
                'class': 'field num_ratings'}).text if n.isdigit()])),  # Extract number of ratings
            # Extract date published as datetime
            standardize_dates(html_tr[i].find(
                'td', {'class': 'field date_pub'}).div.text.strip()),
            str_to_int_rating(html_tr[i].find(
                'td', {'class': 'field rating'}).text),  # Extract user rated
            html_tr[i].find('td', {'class': 'field cover'}).a.get("href")
            # html_tr[i].find('td',{'class':'field title'}).a.text.strip(),
        ]
    except:
        print('Book', i, 'not found')
        pass
# Add a column to determine if book was read
df_my_books['is_read'] = df_my_books['rating'] >= 0

url_prefix = 'https://www.goodreads.com'
df_books_details = pd.DataFrame({'book_description': pd.Series(dtype='str'),
                                 'author_description': pd.Series(dtype='str'),
                                 'genres': pd.Series(dtype='str')
                                 })
