from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

site = ""
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html.parser")