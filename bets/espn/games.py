import os, yaml, csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from argparse import ArgumentParser
import logging as log
fp = os.path.dirname(os.path.realpath(__file__))
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class Data():
    def __init__(self, soup):
        self.soup = soup
        self.game_dat = self.soup.findAll("article",
            {"class": "scoreboard football pregame js-show"})

    def parse_games(self):
        self.games = []
        for game in self.game_dat:
            date_raw = game.find('th', {'class': 'date-time'})['data-date']
            date_obj_utc = datetime.strptime(date_raw, "%Y-%m-%dT%H:%MZ")
            date_obj_etc = date_obj_utc - timedelta(hours=4)
            game_dict = {'game_id': game.attrs['id'],
                         'home_id': game.attrs['data-homeid'],
                         'away_id': game.attrs['data-awayid'],
                         'game_ts': date_obj_etc.strftime('%Y-%m-%d %H:%M'),
                         'week_id': self.week}
            self.games.append(game_dict)
        gd_filneame = '_'.join([str(self.year), str(self.week), '.csv'])
        gd_filepath = '/'.join([fp, 'data/games', gd_filneame])
        with open(gd_filepath, 'w') as output:
            dict_writer = csv.DictWriter(output,
                                         self.games[0].keys(),
                                         quotechar="'",
                                         quoting=csv.QUOTE_NONNUMERIC,)
            dict_writer.writeheader()
            dict_writer.writerows(self.games)
