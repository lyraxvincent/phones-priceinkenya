from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
#import numpy as np

phonenames = ['samsung', 'huawei', 'nokia', 'tecno', 'infinix', 'apple', 'htc', 'google', 'xiaomi', 'motorola',
              'blackberry', 'lg', 'oppo', 'sony', 'gionee', 'oneplus', 'cubot', 'hotwav', 'lenovo', 'vivo',
              'lava', 'realme', 'honor', 'energizer', 'microsoft']

def getlinks(phonename):
    links = []
    site = "https://www.priceinkenya.com/phones/brand/{}".format(phonename)
    links.append(site)  # first link
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if soup.find("ul", {"class":"pagination pagination-sm my-3 justify-content-center"}):   # if there are other pages
        tag_element = soup.find("ul", {"class":"pagination pagination-sm my-3 justify-content-center"})
        for lnk in tag_element.findAll("a", {"href": re.compile("https://www.priceinkenya.com/phones/brand/{}*".format(phonename))}):
            links.append(lnk["href"])

    return links

# calling the function on all phone types
for phone in phonenames:
    getlinks(phone)
    print(f"Added links for [{phone}]")

links = set(links)
print(f"Total number of links: {len(links)}")