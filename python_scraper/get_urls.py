from time import sleep
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def get_child_url(url):
    
    child_urls = []

    source_data = requests.get(url)
    soup = BeautifulSoup(source_data.text, 'html.parser')
    content = soup.find(id='maincontent')
    content_elements = content.find_all('a', class_='product')
    for element in content_elements:
        child_urls.append(element['href'])
    return child_urls

def get_whisky_prices(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    price_html = r.html.find('.price')
    price_list = []
    for price in price_html:
        price_list.append(price.text)
    del price_list[1::2]
    session.close()
    return price_list


def get_all_data(child_urls, price_list):
    i = 0
    dict_list = []
    for url in child_urls:
        source_data = requests.get(url)
        soup = BeautifulSoup(source_data.content, 'html.parser')

        data_categories = soup.find_all("dt", class_=None)
        non_categories = ['Live Auctions', 'Buying', 'Selling', 'Delivery', 'Past Auctions']
       
        whisky_title = soup.find('h1', class_='page-title')
        whisky_price_list = price_list

        categories = ['Title', 'Price']
        for category in data_categories:
            if str(category.text) in str(non_categories):
                pass
            else:
                categories.append(category.text)

        values = [(whisky_title.text).strip(), whisky_price_list[i]]
        data_values = soup.find_all("dd", class_=None)
        for value in data_values:
            values.append(value.text)

        whisky_data = {}

        for category in categories:
            for value in values:
                whisky_data[category] = value
                values.remove(value)
                break

        print(whisky_data)
        dict_list.append(whisky_data)
        i += 1
        sleep(3)
    return dict_list