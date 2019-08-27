import os, yaml, json, requests, time
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class OddsAPI():
    def __init__(self, sport):
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        key_file = os.path.join(self.base_path,'keys.yaml')
        with open(key_file, 'r') as (f):
            keys = yaml.load(f)
        self.key = keys['odds_api']
        self.sport = sport

    def read_json(self, filepath):
        with open(filepath, 'r') as f:
            self.odds_dict = json.load(f)
        return(self.odds_dict)

    def get_json(self):
        log.info('Pulling json from Odds API for: ' + self.sport)
        odds_response = requests.get('https://api.the-odds-api.com/v3/odds',
        params={
            'api_key': self.key,
            'sport': self.sport,
            'region': 'us', # uk | us | au
            'mkt': 'spreads' # h2h | spreads | totals
        })
        self.odds_dict = json.loads(odds_response.text)
        return(self.odds_dict)

    def transform(self, game_dict):
        game_dict['teams'].remove(game_dict['home_team'])
        game_params = {
            'sport': game_dict['sport_nice'],
            'game_date': time.strftime('%Y-%m-%dT%H:%M:%S',
                time.localtime(game_dict['commence_time'])),
            'home': game_dict['home_team'],
            'away': game_dict['teams'][0]
        }
        fp = self.base_path + 'spreads_json/'
        filepath = fp + '{sport}/{game_date}_{home}_{away}/'.format(**game_params)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        for spread in game_dict['sites']:
            spread_dict = {
                'update_ts': time.strftime('%Y-%m-%dT%H:%M:%S',
                    time.localtime(spread['last_update'])),
                'book': spread['site_nice'],
                'spread': max(spread['odds']['spreads']['points'])
            }
            spread_path = filepath + '{book}_{update_ts}.json'.format(**spread_dict)
            with open(spread_path, 'w') as outfile:
                json.dump(spread_dict, outfile, indent=4)

    def main(self):
        self.odds_dict = self.get_json()
        for game_dict in self.odds_dict['data']:
            self.transform(game_dict)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-s", "--sport",
        help="Sport to pull spreads against, i.e. americanfootball_ncaaf")
    args = parser.parse_args()

    OddsAPI(args.sport).main()
