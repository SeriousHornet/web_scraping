import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
               'Safari/537.36'}

# page = input('Enter url: ')
page = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'

pageTree = requests.get(page)
if pageTree.status_code != 200:
    print("request denied")
else:
    print("ok")
    pageSoup = BeautifulSoup(pageTree.text, 'lxml')

    prod_body = pageSoup.select('div[class="product-card__body"]')
