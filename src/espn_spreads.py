import json, time
from bs4 import BeautifulSoup
import boto3


class Parse():
    def __init__(self, soup):
        self.soup = soup
        self.game_dat = self.soup.findAll("article",
            {"class": "scoreboard football pregame js-show"})
        self.main()

    def filter(self, game):
        team_names = game.findAll('span', {'class': 'sb-team-short'})
        teams = [elem.contents[0] for elem in team_names]
        teams_str = ' at '.join(teams)

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
            spread = 'NULL'
            underdog_id = '-1'

        spreads_dict = {'game_id': game.attrs['id'],
                        'team_id': underdog_id,
                        'spread': spread}
        return(spreads_dict)

    def write_s3(self):
        s3 = boto3.resource('s3')
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        filepath = 'espn/spreads/{0}.json'.format(ts)
        s3object = s3.Object('atthletics', filepath)
        s3object.put(
            Body=(bytes(json.dumps(self.spreads, indent=4).encode('UTF-8')))
        )

    def main(self):
        self.spreads = []
        for game in self.game_dat:
            spreads_dict = self.filter(game)
            self.spreads.append(spreads_dict)
        self.write_s3()
