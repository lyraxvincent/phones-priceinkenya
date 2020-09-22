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

# list of phone types to scrap data for
phonenames = ['samsung', 'huawei', 'nokia', 'tecno', 'infinix', 'apple', 'htc', 'google', 'xiaomi', 'motorola',
              'blackberry', 'lg', 'oppo', 'sony', 'gionee', 'oneplus', 'cubot', 'hotwav', 'lenovo', 'vivo',
              'lava', 'realme', 'honor', 'energizer', 'microsoft']


def getlinks(phonename):
    """
    getting links for the different phones through pagination
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

def getdata(link):
    """
    get phones data and save it to a pandas dataframe
    :param link:
    :return: pandas dataframe
    """
    phonesdata = {"phone title": [], "specs": [], "price": [], "rating": [], "specs score": [], "likes": []}
    site = link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    for phone_tag in soup.findAll("div", {"class":"col-md-6 col-lg-4 fancy-border"}):
        phone_tag = phone_tag.find("article")
        phone_title = phone_tag.find("span", {"itemprop": "name", "class":False}).get_text()
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

        # save data to pandas dataframe
        df = pd.DataFrame(phonesdata)
        #df.to_csv("phonesdata.csv", index=False)
        return df