import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
               'Safari/537.36'}

# specify the URL
base_url = "https://www.fotmob.com/match/"
# match = str(input('Please enter the match ID: '))
match = str(3370551)
url = base_url + match

# send a request to the URL and get the HTML response
pageTree = requests.get(url, headers=headers)

# parse the HTML response using BeautifulSoup
pageSoup = BeautifulSoup(pageTree.content, 'lxml')

# find all the script tags
scripts = pageSoup.find_all('script')

# check if any matching tags were found
if len(scripts) == 0:
    print("No matching tags were found.")
else:
    print("Tags found.")

# get the last string
strings = scripts[-1].string
# print(strings)

# delete the last bit, to get just the useful information
ind_end = strings.index('"page":')
json_data = strings[:ind_end]
repl = "}"
json_data = json_data[:-1] + repl
#

raw_data = json.loads(json_data)
# print(type(raw_data))


df_general = raw_data["props"]["pageProps"]["general"]
# print(len(df_general.items()))
# print(df_general.items())
df_content = raw_data["props"]["pageProps"]["content"]
df_shots = df_content["shotmap"]["shots"]
print(type(df_shots))
shots_dict = {}
for item in df_shots:
    for i in item:
        shots_dict.update(item)
    shots_dict.update(item)

print(shots_dict)
# shot_df = pd.DataFrame.from_dict(shots_dict)
# print(len(shots_dict.keys()))
# print(shot_df)
# print(len(df_shots.items()))
# print(shots.items())
# df_shots = df_content["shotmap"]["shots"]
# print(df_shots)
