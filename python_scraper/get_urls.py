from time import sleep
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


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


def get_all_data(child_urls, price_list):
    dict_list = []
    for i, url in enumerate(child_urls[:2]):
        source_data = requests.get(url)
        soup = BeautifulSoup(source_data.content, 'html.parser')

        data_categories = soup.find_all("dt", class_=None)
        non_categories = ['Live Auctions', 'Buying', 'Selling', 'Delivery', 'Past Auctions']
       
        whisky_title = soup.find('h1', class_='page-title')
        whisky_price_list = price_list

        categories = [category.text for category in data_categories if str(category.text) not in str(non_categories)]
        all_categories = ['Title', 'Price'] + categories

        values = [(whisky_title.text).strip(), whisky_price_list[i]]
        data_values = soup.find_all("dd", class_=None)
        for value in data_values:
            values.append(value.text)

        whisky_data = {}

        for category in all_categories:
            for value in values:
                whisky_data[category] = value
                values.remove(value)
                break

        print(whisky_data)
        dict_list.append(whisky_data)
        sleep(3)
    return dict_list
