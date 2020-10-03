from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

# a function to clean phone titles so their search can yield better results
def cleantitle(phonetitle):
    if str(phonetitle).endswith("GB") or "/" in str(phonetitle):
        phonetitle = ' '.join(phonetitle.split()[:-1])
    if "(" in str(phonetitle):
        phonetitle = phonetitle.split("(")[0].strip()
        return phonetitle
    else:
        return phonetitle


# read in csv file
df = pd.read_csv("csv files/phonesdata.csv")
df_ = df.copy()     # make copy to avoid editing the original phone titles
df_['Phone Title'] = df_['Phone Title'].apply(cleantitle)
df_['Phone Title'] = df_['Phone Title'].apply(lambda s: s.replace(" ", "+"))    # link syntax
phonenames = list(df_['Phone Title'])

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
df.to_csv("csv files/phonesdata_with_pfj.csv", index=False)