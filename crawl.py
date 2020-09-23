from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

""" starter code snippet:
site= "https://www.priceinkenya.com/phones"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html.parser")
"""

def getlinks(phonename):
    """
    get links for the different phones through pagination
    without going into specific webpages
    get links from the 'ul' pagination element
    :param phonename:
    :return: list of links
    """

    links = []
    site = "https://www.priceinkenya.com/phones/brand/{}".format(phonename)
    links.append(site)  # first link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if soup.find("ul", {"class": "pagination pagination-sm my-3 justify-content-center"}):  # if there are other pages
        tag_element = soup.find("ul", {"class": "pagination pagination-sm my-3 justify-content-center"})
        for lnk in tag_element.findAll("a", {
            "href": re.compile("https://www.priceinkenya.com/phones/brand/{}*".format(phonename))}):
            links.append(lnk["href"])

    return links


# list of phone types to scrap data for
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
phonesdata = {"phone title": [], "specs": [], "price": [], "rating": [], "specs score": [], "likes": []}

for link in links:
    site = link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    print(f"Getting phones data in [{link}]")

    for phone_tag in soup.findAll("div", {"class":"col-md-6 col-lg-4 fancy-border"}):
        phone_tag = phone_tag.find("article")
        phone_title = phone_tag.find("span", {"itemprop": "name", "class":False}).get_text()
        phonesdata["phone title"].append(phone_title)
        specs = phone_tag.find("div", {"class": "mb-4"}).get_text()
        phonesdata["specs"].append(specs)
        try:
            price = phone_tag.find("div", {"class": "h5 d-inline-block m-0 my-1"}).get_text()
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


# save data to csv file
df = pd.DataFrame(phonesdata)
df.to_csv("phonesdata.csv", index=False)
print("Saved dataframe.")
