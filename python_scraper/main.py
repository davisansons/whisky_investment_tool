from get_urls import get_child_url, get_all_data, get_whisky_prices


def get_url():
    return "https://www.whiskyshop.com/auctions/ended?product_list_order=price_desc&auction_ended=August+2019"

#get_child_url(url)

#get_whisky_prices(url)


if __name__ == "__main__":
    url = get_url()
    get_all_data(get_child_url(url), get_whisky_prices(url))
