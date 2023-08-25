from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
from datetime import datetime

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from helpers import * 

url = 'https://www.goodreads.com/review/list/142380450-mauricio-pujol' # This is my profile containing all read and unread books
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
html_tr = soup.find_all("tr")
df_my_books = pd.DataFrame({'title': pd.Series(dtype='str'), #This defines the structure for the dataframe to store scraped data
                   'author': pd.Series(dtype='str'),
                   'pages': pd.Series(dtype='int'),
                   'avg_rating': pd.Series(dtype='float'),
                   'num_ratings': pd.Series(dtype='int'),
                   'date_pub': pd.Series(dtype='str'),
                   'rating': pd.Series(dtype='int'),
                   'cover_link': pd.Series(dtype='str')
                   #'c': pd.Series(dtype='float')
                })
for i in range(0,len(html_tr)):
    try:
        df_my_books.loc[len(df_my_books.index)] = [
            html_tr[i].find('td',{'class':'field title'}).a.text.strip(), # Extract book title
            html_tr[i].find('td',{'class':'field author'}).a.text.strip(), # Extract book author
            int(re.search(r'[\d]+',html_tr[i].find('td',{'class':'field num_pages'}).text).group()), # Extract book number of pages
            float(re.search(r'[\d+\.\d+]+',html_tr[i].find('td',{'class':'field avg_rating'}).text).group()), # Extract average rating
            int(''.join([n for n in html_tr[i].find('td',{'class':'field num_ratings'}).text if n.isdigit()])), # Extract number of ratings
            standardize_dates(html_tr[i].find('td',{'class':'field date_pub'}).div.text.strip()), # Extract date published as datetime
            str_to_int_rating(html_tr[i].find('td',{'class':'field rating'}).text), # Extract user rated
            html_tr[i].find('td',{'class':'field cover'}).a.get("href")
            #html_tr[i].find('td',{'class':'field title'}).a.text.strip(),                            
            ]
    except:
        pass
df_my_books['is_read'] = df_my_books['rating'] >= 0 # Add a column to determine if book was read
## Obtain book specific genres
url_prefix = 'https://www.goodreads.com'
df_books_details = pd.DataFrame({'book_description': pd.Series(dtype='str'),
                   'author_description': pd.Series(dtype='str'),
                   'genres': pd.Series(dtype='str')
                })

for title,book_url in df_my_books[['title','cover_link']].values:
    page = urlopen(url_prefix+book_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    html_div = soup.find_all('div',{'class':'DetailsLayoutRightParagraph__widthConstrained'})
    # debug start
    #pretty_soup = soup.prettify()
    #with open(title[0:3]+".txt","w") as out:
    #    for i in range(0, len(pretty_soup)):
    #        try:
    #            out.write(pretty_soup[i])
    #        except:
    #            pass
    #print()
    # debug end
    book_description =html_div[0].text
    author_description = html_div[1].text
    try:
        genres_str = ''
        genres_soup = list(soup.find('ul',{'class':'CollapsableList',"aria-label": True}).span)
        for genre in genres_soup:
            if genre.text != 'Genres':
                genres_str = genres_str + genre.text + ', '
    except:
        genres_str = None
    df_books_details.loc[len(df_books_details.index)] = [book_description,author_description,genres_str]

df_my_books 