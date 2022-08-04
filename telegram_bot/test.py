from bs4 import BeautifulSoup
import pprint
import requests
from lxml import etree
import pandas as pd
import xml.etree.ElementTree as ET
from pycbrf.toolbox import ExchangeRates
import time
from urllib.request import urlopen


url_sbr = 'http://www.cbr.ru/scripts/XML_daily.asp'
one = requests.get(url_sbr)
usd_rate = ET.fromstring(one.text)
for i in usd_rate:
    if i[1].text == 'USD':
        print(i[1].text, i[4].text)
    if i[1].text == 'EUR':
        print(i[1].text, i[4].text)


