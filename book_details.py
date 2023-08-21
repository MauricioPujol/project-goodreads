from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

df_books_details = pd.DataFrame({'cover_link': pd.Series(dtype='str'),
                    'book_description': pd.Series(dtype='str'),
                   'author_description': pd.Series(dtype='str'),
                   'genres': pd.Series(dtype='str')
                })


url = '/book/show/141263.Ars_ne_Lupin_versus_Herlock_'
url_prefix = 'https://www.goodreads.com'
page = urlopen(url_prefix+url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
html_div = soup.find_all('div',{'class':'DetailsLayoutRightParagraph__widthConstrained'})
book_description =html_div[0].text
author_description = html_div[1].text
genres_soup = list(soup.find('ul',{'class':'CollapsableList',"aria-label": True}).span)
genres_str = ''
for genre in genres_soup:
    if genre != 'Genres':
        genres_str = genres_str + genre.text + ','

df_books_details.loc[len(df_books_details.index)] = [url,book_description,author_description,genres_str)]


            #html_tr[i].find('td',{'class':'field title'}).a.text.strip(),                            
            
book_description
author_description
author_description
