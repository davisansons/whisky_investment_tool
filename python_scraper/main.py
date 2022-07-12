from get_urls import get_child_url, get_all_data

url = "https://www.whiskyshop.com/auctions/ended?product_list_order=price_desc&auction_ended=August+2019"

child_url = "https://www.whiskyshop.com/auctions/a11265-macallan-1995-13-year-old-single-cask-14016-easter-elchies-2009"



# print(get_child_url(url))

print(get_all_data(get_child_url(url)))