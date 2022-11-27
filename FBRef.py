import requests
from bs4 import BeautifulSoup

URL = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
results.prettify()
