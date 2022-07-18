from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
from pathlib import Path


def get_child_url(url):
    src_data = requests.get(url)
    soup = BeautifulSoup(src_data.text, 'html.parser')
    content_elements = soup.find(id='maincontent').find_all('a', class_='product')
    return [x['href'] for x in content_elements]


def get_whisky_prices(url):
    with HTMLSession() as session:
        r = session.get(url)
        r.html.render(sleep=1, keep_page=True, scrolldown=1)
        price_html = r.html.find('.price')
        price_list = [x.text for x in price_html]
    return price_list[0::2]

def get_whisky_titles(url):
    with HTMLSession() as session:
        r = session.get(url)
        r.html.render(sleep=1, keep_page=True, scrolldown=1)
        title_html = r.html.find('.product-item-link')
        title_list = [x.text for x in title_html]
    return title_list[0::2]


def get_all_data(child_urls, price_list, title_list):
    whisky_data = pd.DataFrame([])
    for i, url in enumerate(child_urls[:350]):
        source_data = requests.get(url)
        soup = BeautifulSoup(source_data.content, 'html.parser')

        data_categories = soup.find_all("dt", class_=None)
        non_categories = ['Live Auctions', 'Buying', 'Selling', 'Delivery', 'Past Auctions']
       
        whisky_title = title_list
        whisky_price_list = price_list

        categories = ['Title', 'Price'] + [category.text for category in data_categories if str(category.text) not in str(non_categories)]

        values = [whisky_title[i], whisky_price_list[i]]
        data_values = soup.find_all("dd", class_=None)
        for value in data_values:
            values.append(value.text)
        
        new_data = pd.DataFrame([values], columns=categories)
    
        whisky_data = pd.concat([whisky_data, new_data], sort=False, ignore_index=True).fillna('null')
        print(whisky_data)
        sleep(0.5)
    print(whisky_data)
    whisky_data.to_csv("whisky_data.csv", index=False, encoding='utf-8')
    return whisky_data
