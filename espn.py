import os
from bs4 import BeautifulSoup
from datetime import datetime
from argparse import ArgumentParser
import pandas as pd
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class ESPN():
    def __init__(self, week):
        self.week = week
        os.system("phantomjs scrape_espn.js")
        self.soup = BeautifulSoup(open("espn.html"), "html.parser")
        self.game_dat = self.soup.findAll("article", {"class": "scoreboard football pregame js-show"})

    def get_games(self):
        games = []
        for game in self.game_dat:
            date_raw = game.find('th', {'class': 'date-time'})['data-date']
            time_raw = game.find('span', {'class': 'time', 'data-dateformat':'time1'}).contents[0]
            date_obj = datetime.strptime(date_raw, "%Y-%m-%dT%H:%MZ")
            time_obj = datetime.strptime(time_raw, '%I:%M %p ET')

            game_ts_obj = datetime(
                date_obj.year,
                date_obj.month,
                date_obj.day,
                time_obj.hour,
                time_obj.minute
            )

            game_dict = {
                'game_id': game.attrs['id'],
                'home_id': game.attrs['data-homeid'],
                'away_id': game.attrs['data-awayid'],
                'game_ts': game_ts_obj.strftime('%Y-%m-%d %H:%M'),
                'week_id': self.week
            }
            games.append(game_dict)

        self.games_data = pd.DataFrame(games)
        self.games_data = self.games_data[
            ['game_id', 'home_id', 'away_id', 'game_ts', 'week_id']
        ]
        self.games_data.to_csv('game_data/games.csv', index=False)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-w", "--week",
        help="Week to pull ESPN data for")
    args = parser.parse_args()
    ESPN(args.week).get_games()
