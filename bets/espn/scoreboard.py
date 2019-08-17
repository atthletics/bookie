import os, yaml, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from argparse import ArgumentParser
import logging as log
fp = os.path.dirname(os.path.realpath(__file__))
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class URLOpener():
    '''
    Gets BeautifulSoup object from inputted URL. Waits for the page to render
    first before parsing the HTML.
    '''
    def __init__(self, url):
        log.info('Initializing headless browser')
        self.url = url
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def get_soup(self):
        log.info('Opening page for :' + self.url)
        self.browser.get(self.url)
        log.info('Parsing HTML')
        html = self.browser.page_source
        self.soup = BeautifulSoup(html, 'lxml')
        return(self.soup)

class Scoreboard():
    '''
    Pulls games and spreads data from ESPN scoreboard page
    '''
    def __init__(self, year, week):
        self.year = year
        self.week = week
        with open(fp + '/config.yaml', 'r') as (f):
            self.espn_config = yaml.load(f, Loader=yaml.FullLoader)
        self.params = {'year': self.year,
                       'week': self.week}

    def get_game_soup(self):
        self.games_url = self.espn_config['games_url'].format(**self.params)
        self.soup = URLOpener(self.games_url).get_soup()
        self.game_dat = self.soup.findAll("article",
            {"class": "scoreboard football pregame js-show"})
        return(self.game_dat)

    def parse_game_data(self):
        self.games = []
        for game in self.game_dat:
            date_raw = game.find('th', {'class': 'date-time'})['data-date']
            time_raw = game.find('span',
                {'class': 'time', 'data-dateformat':'time1'}).contents[0]
            date_obj = datetime.strptime(date_raw, "%Y-%m-%dT%H:%MZ")
            time_obj = datetime.strptime(time_raw, '%I:%M %p ET')
            game_ts_obj = datetime(
                date_obj.year,
                date_obj.month,
                date_obj.day,
                time_obj.hour,
                time_obj.minute)
            game_dict = {'game_id': game.attrs['id'],
                         'home_id': game.attrs['data-homeid'],
                         'away_id': game.attrs['data-awayid'],
                         'game_ts': game_ts_obj.strftime('%Y-%m-%d %H:%M'),
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

    def parse_spread_data(self):
        self.spreads = []
        for game in self.game_dat:
            try:
                spread_raw = game.find('th', {'class': 'line'}).contents[0]
            except AttributeError:
                spread_raw = 'N/A 0'
            spread_split = str.split(spread_raw, ' ')
            spreads_dict = {'game_id': game.attrs['id'],
                            'espn_short_name': spread_split[0],
                            'spread': spread_split[1]}
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

    def main(self, selector):
        self.get_game_soup()
        if selector.lower() == 'games':
            self.parse_game_data()
        elif selector.lower() == 'spreads':
            self.parse_spread_data()
        else:
            self.parse_game_data()
            self.parse_spread_data()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-y", "--year",
        help="Year to pull ESPN data for")
    parser.add_argument("-w", "--week",
        help="Week to pull ESPN data for")
    parser.add_argument('-s', "--selector",
        help="Select games or spreads",
        default='Both')
    args = parser.parse_args()
    Scoreboard(args.year, args.week).main(args.selector)
