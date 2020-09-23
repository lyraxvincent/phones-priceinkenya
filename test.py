from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
#import re
import numpy as np
import pandas as pd

phonesdata = {"phone title": [], "specs": [], "price": [], "rating": [], "specs score": [], "likes": []}
site = "https://www.priceinkenya.com/phones/brand/lg"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html.parser")

for phone_tag in soup.findAll("div", {"class": "col-md-6 col-lg-4 fancy-border"}):
    phone_tag = phone_tag.find("article")
    phone_title = phone_tag.find("span", {"itemprop": "name", "class": False}).get_text()
    phonesdata["phone title"].append(phone_title)
    specs = phone_tag.find("div", {"class": "mb-4"}).get_text()
    phonesdata["specs"].append(specs)
    try:
        price = phone_tag.find("span", {"class": "text-danger"}).get_text()
        phonesdata["price"].append(price)
    except:
        price = np.nan
        phonesdata["price"].append(price)

    rating = phone_tag.find("span", {"title": "Rating", "class": "mr-3"}).get_text()
    phonesdata["rating"].append(rating)
    specs_score = phone_tag.find("span", {"title": "Specs score"}).get_text()
    phonesdata["specs score"].append(specs_score)
    likes = phone_tag.find("div", {"class": "likes"}).find("like")[":likes-count"]
    phonesdata["likes"].append(likes)


df = pd.DataFrame(phonesdata)
print(df.tail())