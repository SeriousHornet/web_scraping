import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

pd.set_option('display.max_columns', 50)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 ' 
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

# delete the last bit, to get just the useful information
ind_end = strings.index('"page":')
json_data = strings[:ind_end]
repl = "}"
json_data = json_data[:-1] + repl

raw_data = json.loads(json_data)

general = raw_data["props"]["pageProps"]["general"]
content = raw_data["props"]["pageProps"]["content"]
print(general.keys())
print(general['leagueRoundName'])
# looker = df_content['stats']['stats'][1]
# print(len(looker))
# print(type(looker))
# print(looker['stats'])
# df_looker = pd.DataFrame(looker['stats'])
# print(df_looker)

shots = content["shotmap"]["shots"]

df_shots = pd.DataFrame(shots)

float_conv = {'x': float, 'y': float, 'min': int, 'blockedX': float, 'blockedY': float, 'expectedGoals': float,
              'expectedGoalsOnTarget': float, 'goalCrossedY': float, 'goalCrossedZ': float}
df_shots = df_shots.astype(float_conv)
df_shots['conv_x'] = df_shots['x'] * 1.142857142857143
df_shots['conv_y'] = df_shots['y'] * 1.176470588235294
df_shots['xG'] = df_shots['expectedGoals'] * 200
# df_shots['team'] =

fig, axs = plt.subplots(figsize=(6, 8))
fig.set_facecolor('#3e3e40')
axs.patch.set_facecolor('#3e3e40')

pitch = Pitch(half=True,
              pitch_color='#3e3e40',
              line_color='#aba9a8')

pitch.draw(ax=axs)
plt.gca().invert_yaxis()


def plotting(df):
    for x in range(len(df['x'])):
        X, Y, xG = df['conv_x'][x], df['conv_y'][x], df['xG'][x]
        if df['eventType'][x] == "Goal":
            plt.scatter(X, Y, c='lime')
        if df['eventType'][x] == "AttemptSaved":
            plt.scatter(X, Y, c='darkorange')
        if df['eventType'][x] == "Miss":
            plt.scatter(X, Y, c='r')
    return

# plotting(df_shots)
# plt.show()
# print(df)
# print(new_shots)
# print(shots_dict)
# shot_df = pd.DataFrame.from_dict(shots_dict)
# print(len(shots_dict.keys()))
# print(shot_df)
# print(len(df_shots.items()))
# print(shots.items())
# df_shots = df_content["shotmap"]["shots"]
# print(df_shots)
