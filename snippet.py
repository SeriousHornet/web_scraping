import requests
from bs4 import BeautifulSoup

# specify the URL
url = "https://www.fotmob.com/match/3370551/matchfacts/argentina-vs-australia"

# send a request to the URL and get the HTML response
response = requests.get(url)

# parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# find all the circle tags with the ID "circle" in the HTML response
tags = soup.find_all('circle', id='circle')

# print the scraped data
for circle in tags:
    print(circle)

# check if any matching tags were found
if len(tags) == 0:
    print("No matching tags were found.")
else:
    # print the scraped data
    for tag in tags:
        print(tag)

# print the cx and cy attributes of each circle tag
for circle in tags:
    print(circle.get('cx'))
    print(circle.get('cy'))
