import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
               'Safari/537.36'}

# page = input('Enter url: ')
# page = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'
page = 'https://www.fotmob.com/match/3370551/matchfacts/argentina-vs-australia'
pageTree = requests.get(page, headers=headers)
if pageTree.status_code != 200:
    print("request denied")
else:
    print("ok")
    pageSoup = BeautifulSoup(pageTree.text, 'html.parser')
    print(type(pageSoup))
    # print(pageSoup.prettify())
    shot_div = pageSoup.find_all('circle', id='circle')#[class="results__body"]')
    # shot_div = pageSoup.find_all(attrs={'class': 'css-kgyj9i-PitchSVGWrapper'})
    print(type(shot_div))
    print(shot_div)
    # for shot in shot_div:
    #     print(shot.get('cx'))
    #     print(shot.get('cy'))

    # body = pageSoup.select('div[class="product-card__body"]')
    # print(pageSoup.find_all('div', attrs={'class': 'banner-node'}))#[class="banner-node css-gb9zhi"]')


# html = '<tr id="history_row_938220" style="" class="admin-bookings-table-row bookings-history-row  paid   ">'
#css-62w8ud-FullscreenShotmapContainer-applyLightHover-ShotmapAnimations-commonShotMapContainer e1786a3a20
# soup = BeautifulSoup(html, 'html.parser')
# res = soup.find_all(attrs={'class': 'paid'})
# print(res)
