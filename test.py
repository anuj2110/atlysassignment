# import requests
# from bs4 import BeautifulSoup

# url = "https://dentalstall.com/shop/page/1"

# response = requests.get(url)

# soup = BeautifulSoup(response.content, "html.parser")

# results = soup.find(id="mf-shop-content")

# products = results.find_all("div", class_="product-inner clearfix")

# for product in products:
#     print(product.find("div", class_="mf-product-thumbnail").find("img",
#           class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail").get("data-lazy-src"))
#     print(product.find("div",class_="mf-product-details").find("h2",class_="woo-loop-product__title").text)
#     print(product.find("div",class_="mf-product-price-box").find("span",class_="woocommerce-Price-amount amount").find("bdi").text)
    

import itertools

nested_list_with_empty = [[1, 2, 3], [], [4, 5], [], [6, 7, 8]]
flattened_list = list(itertools.chain.from_iterable(nested_list_with_empty))
print(flattened_list)