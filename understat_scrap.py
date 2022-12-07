import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

pd.set_option('display.max_columns', 50)
base_url = 'https://understat.com/match/'
# match = str(input('Please enter the match id: '))
# url = base_url + match
url = 'https://understat.com/match/19773'

res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')

scripts = soup.findAll('script')

strings = scripts[1].string
ind_start = strings.index("('") + 2
ind_end = strings.index("')")

json_data = strings[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')
raw_data = json.loads(json_data)

data_home = raw_data['h']
data_away = raw_data['a']
home = pd.DataFrame.from_dict(data_home)
away = pd.DataFrame.from_dict(data_away)

float_conv = {'X': float, 'Y': float, 'xG': float, 'minute': int, 'h_goals': int, 'a_goals': int}

away = away.astype(float_conv)
home = home.astype(float_conv)

away['x'] = away['X'] * 120
away['y'] = away['Y'] * 80
away['xg'] = away['xG'] * 250

home['x'] = home['X'] * 120
home['y'] = home['Y'] * 80
home['xg'] = home['xG'] * 250

fig, axs = plt.subplots(figsize=(6, 8))
fig.set_facecolor('#3e3e40')
axs.patch.set_facecolor('#3e3e40')

pitch = Pitch(half=True,
              pitch_color='#3e3e40',
              line_color='#aba9a8')

pitch.draw(ax=axs)
plt.gca().invert_yaxis()


def plotting(df):
    for x in range(len(df['X'])):
        X, Y, xG = df['x'][x], df['y'][x], df['xg'][x]
        if df['result'][x] == "Goal":
            plt.scatter(X, Y, c='lime', s=xG)
        if df['result'][x] == "SavedShot":
            plt.scatter(X, Y, c='r', s=xG)
        if df['result'][x] == "BlockedShot":
            plt.scatter(X, Y, c='darkorange', s=xG)
    return


h_team = home['h_team'][0]
a_team = away['a_team'][0]

team = input("Select home or away team: ")
if team == 'home':
    plotting(home)
    plt.title(f'{h_team} shots \n vs. {a_team}', color='white', size=20)

if team == 'away':
    plotting(away)
    plt.title(f'{a_team} shots \n vs. {h_team}', color='white', size=20)


plt.show()