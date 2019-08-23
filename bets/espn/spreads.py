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

    def parse_spreads(self):
        self.spreads = []
        for game in self.game_dat:
            team_names = game.findAll('span', {'class': 'sb-team-short'})
            teams = [elem.contents[0] for elem in team_names]
            teams_str = ' at '.join(teams)
            log.info('Getting spread for ' + teams_str)
            try:
                spread_raw = game.find('th', {'class': 'line'}).contents[0]
            except AttributeError:
                spread_raw = 'N/A 0'
            spread_split = str.split(spread_raw, ' ')
            favorite = spread_split[0]
            try:
                ids = [game.attrs['data-awayid'], game.attrs['data-homeid']]
                short_names = game.findAll('span', {'class': 'sb-team-abbrev'})
                short_names = [elem.contents[0] for elem in short_names]
                del_idx = short_names.index(favorite)
                ids.pop(del_idx)
                underdog_id = ids[0]
                spread = abs(float(spread_split[1]))
            except ValueError:
                log.info('No spread available: ' + teams_str)
                spread = 0
                underdog_id = '-1'
            spreads_dict = {'game_id': game.attrs['id'],
                            'team_id': underdog_id,
                            'spread': spread}
            self.spreads.append(spreads_dict)
        sd_filename = '_'.join([str(self.year), str(self.week), '.csv'])
        sd_filepath = '/'.join([fp, 'data/spreads', sd_filename])
        with open(sd_filepath, 'w') as output:
            dict_writer = csv.DictWriter(output,
                                         self.spreads[0].keys(),
                                         quotechar="'",
                                         quoting=csv.QUOTE_NONNUMERIC,)
            dict_writer.writeheader()
            dict_writer.writerows(self.spreads)
