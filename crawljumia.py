from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

def getlinks(phonename):
    """
    get links for the different phones through pagination
    without going into specific webpages
    get links from the 'ul' pagination element
    :param phonename:
    :return: list of links
    """

    links = []
    site = "https://www.jumia.co.ke/smartphones/{}/?viewType=list".format(phonename)
    links.append(site)  # first link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if soup.find("div", {"class": "pg-w -pvxl"}):  # if there are other pages
        tag_element = soup.find("div", {"class": "pg-w -pvxl"})
        for lnk in tag_element.findAll("a", {"href": re.compile("/smartphones/{}*".format(phonename))}):
            links.append("https://www.jumia.co.ke" + lnk["href"])

    return links


# list of phone types to scrap data for
#phonenames = ['apple', 'huawei', 'infinix', 'samsung', 'nokia', 'xiaomi', 'oppo', 'tecno', 'ulefone', 'vivo', 'sony']
phonenames = ['samsung', 'huawei', 'nokia', 'tecno', 'infinix', 'apple', 'htc', 'google', 'xiaomi', 'motorola',
              'blackberry', 'lg', 'oppo', 'sony', 'gionee', 'oneplus', 'cubot', 'hotwav', 'lenovo', 'vivo',
              'lava', 'realme', 'honor', 'energizer', 'microsoft']


# calling the function on all phone types
links = []
for phone in phonenames:
    lnks = getlinks(phone)
    for lnk in lnks:
        links.append(lnk)
    print(f"Added links for [{phone}]")

# filter links to remove duplicates
links = set(links)
print(f"\nTotal number of links: {len(links)}")


# getting phones data for all collected links
phonesdata = {"phone title": [], "price": [], "old price": []}


for link in links:
    site = link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    print(f"Getting phones data in [{link}]")

    for phonetag in soup.findAll("article", {"class": "prd _fl c-prd"}):
        nametag = phonetag.find("div", {"class": "main"})
        phonename = nametag.find("h3", {"class": "name"}).get_text()
        phonesdata['phone title'].append(phonename)
        pricetag = phonetag.find("div", {"class": "sd"})
        price = pricetag.find("div", {"class": "prc"}).get_text()
        phonesdata['price'].append(price)
        # get old price before discount
        try:
            oldprice = pricetag.find("div", {"class": "s-prc-w"})
            oldprice = oldprice.find("div", {"class": "old"}).get_text()
            phonesdata['old price'].append(oldprice)
        except:
            oldprice = np.nan
            phonesdata['old price'].append(oldprice)


# save data to csv file
df = pd.DataFrame(phonesdata)
df.to_csv("jumiadata.csv", index=False)
print("Saved dataframe.")