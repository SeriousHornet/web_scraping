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
match = str(input('Please enter the match ID: '))
# match = str(3370551)
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

# extracting needed data from raw data
general = raw_data["props"]["pageProps"]["general"]
roundName = general['leagueRoundName']
homeTeam = general['homeTeam']['name']
homeTeamID = general['homeTeam']['id']
awayTeam = general['awayTeam']['name']
awayTeamID = general['awayTeam']['id']
content = raw_data["props"]["pageProps"]["content"]
shots = content["shotmap"]["shots"]

df_shots = pd.DataFrame(shots)
float_conv = {'x': float, 'y': float, 'min': int, 'blockedX': float, 'blockedY': float, 'expectedGoals': float,
              'expectedGoalsOnTarget': float, 'goalCrossedY': float, 'goalCrossedZ': float}
df_shots = df_shots.astype(float_conv)
df_shots['conv_x'] = df_shots['x'] * 1.142857142857143
df_shots['conv_y'] = df_shots['y'] * 1.176470588235294
df_shots['xG'] = df_shots['expectedGoals'] * 200

home_df = df_shots[df_shots.teamId == homeTeamID]
away_df = df_shots[df_shots.teamId == awayTeamID]


def call_fig():
    fig, axs = plt.subplots(figsize=(6, 8))
    fig.set_facecolor('#3e3e40')
    axs.patch.set_facecolor('#3e3e40')

    pitch = Pitch(half=True,
                  pitch_color='#3e3e40',
                  line_color='#aba9a8')

    pitch.draw(ax=axs)
    plt.gca().invert_yaxis()


def plotting(df):
    for i, row in df.iterrows():
        X, Y, xG = df.loc[i, 'conv_x'], df.loc[i, 'conv_y'], df.loc[i, 'xG']
        if df.loc[i, 'eventType'] == "Goal":
            plt.scatter(X, Y, c='lime', marker='*', s=xG)
        if df.loc[i, 'eventType'] == "AttemptSaved":
            plt.scatter(X, Y, c='darkorange', s=xG)
        if df.loc[i, 'eventType'] == "Miss":
            plt.scatter(X, Y, c='r', s=xG)
    return


call_fig()
team = input("Select home or away team: ")
if team == 'home':
    plotting(home_df)
    plt.title(f"{homeTeam} shots \n vs. {awayTeam} in {roundName}", fontsize=20, color="white")
    plt.savefig(f'Shots of {homeTeam} vs. {awayTeam} in {roundName}.png',
                transparent=False,
                dpi=1000)
if team == 'away':
    plotting(away_df)
    plt.title(f'{awayTeam} shots \n vs. {homeTeam}', fontsize=20, color="white")
    plt.savefig(f'Shots of {awayTeam} vs. {homeTeam} in {roundName}.png',
                transparent=False,
                dpi=1000)