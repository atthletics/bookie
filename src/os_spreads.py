import time, boto3, json
from bs4 import BeautifulSoup

class Parse():
    def __init__(self, soup):
        self.soup = soup
        self.games_final = self.soup.findAll("div", {"class": "matchup final"})
        self.games_pre = self.soup.findAll("div", {"class": "matchup pre"})
        self.main()

    def parse_divs(self, matchup):
        teams_raw = matchup.findAll('div', {'class': 'team-header', 'class': 'city'})
        spreads_raw = matchup.findAll('div', {'class': 'value'})
        underdog_idx = [i for i,spread in enumerate(spreads_raw) if float(spread.contents[0]) > 0][0]
        matchup_dict = {
            'away_team' : teams_raw[0].contents[0],
            'home_team' : teams_raw[1].contents[0],
            'underdog'  : teams_raw[underdog_idx].contents[0],
            'spread'    : float(spreads_raw[underdog_idx].contents[0])
        }
        scores_raw = matchup.findAll('td', {'class' : 'segment'})
        if matchup.find('div', {'class' : 'status'}).contents[0] == 'final':
            matchup_dict['away_score'] = int(scores_raw[4].contents[0])
            matchup_dict['home_score'] = int(scores_raw[9].contents[0])
        return(matchup_dict)

    def write_s3(self, dictionary, filepath):
        s3 = boto3.resource('s3')
        s3object = s3.Object('atthletics', filepath)
        s3object.put(
            Body=(bytes(json.dumps(dictionary, indent=4).encode('UTF-8')))
        )

    def main(self):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        self.games_final_data = []
        for matchup in self.games_final:
            self.games_final_data.append(self.parse_divs(matchup))
        scores_fp = 'oddsshark/scores/{0}.json'.format(ts)
        self.write_s3(self.games_final_data, scores_fp)

        self.games_pre_data = []
        for matchup in self.games_pre:
            self.games_pre_data.append(self.parse_divs(matchup))
        spreads_fp = 'oddsshark/spreads/{0}.json'.format(ts)
        self.write_s3(self.games_pre_data, spreads_fp)
