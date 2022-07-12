from get_urls import get_child_url, get_all_data, get_whisky_prices

url = "https://www.whiskyshop.com/auctions/ended?product_list_order=price_desc&auction_ended=August+2019"



#get_child_url(url)

#get_whisky_prices(url)

get_all_data(get_child_url(url), get_whisky_prices(url))