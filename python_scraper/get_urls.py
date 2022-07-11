from bs4 import BeautifulSoup
import requests

def get_urls_function(url):
    request_url = requests.get(url)
    soup = BeautifulSoup(request_url.text, "html.parser")
    url_list = []
    results = soup.find(id='maincontent')
    results_elements = results.find_all("a", class_="product")
    for element in results_elements:
        url_list.append(element["href"])
    print(url_list)
    return url_list

