from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import string

# read in csv file
df = pd.read_csv("phonesdata.csv")
df['Phone Title'] = df['Phone Title'].apply(lambda s: ''.join([l for l in s if l not in string.punctuation]))
df['Phone Title'] = df['Phone Title'].apply(lambda s: ' '.join(s.split()[:-1]))
df['Phone Title'] = df['Phone Title'].apply(lambda s: s.replace(" ", "+"))
phonenames = list(df['Phone Title'])

prices = []
for i, phonename in enumerate(phonenames):
    site = "https://www.jumia.co.ke/catalog/?q={}".format(phonename)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    try:
        price = soup.find("div", {"class": "prc"}).get_text()
        prices.append(price)
        print(f"{i}:Added price for [{phonename}]")
    except:
        price = np.nan
        print(f"{i}:Price for [{phonename}] unavailable.")

# add prices column to dataframe
df['PriceJumia(Kshs)'] = pd.Series(prices)
df.to_csv("phonesdata2.csv", index=False)