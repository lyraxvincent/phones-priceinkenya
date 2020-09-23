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

    try:
        price = phone_tag.find("div", {"class": "h5 d-inline-block m-0 my-1"}).get_text()
        #phonesdata["price"].append(price)
        print(price)
    except:
        price = np.nan
        print(price)
        #phonesdata["price"].append(price)