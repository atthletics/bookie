import time, boto3, json
from bs4 import BeautifulSoup
        
class Game():
    def __init__(self, game_soup):
        self.game_soup = game_soup
        keys = [
            'game_status',
            'game_ts',
            'away_team', 
            'home_team', 
            'underdog', 
            'spread',
            'away_score',
            'home_score',
            'winner',
            'is_upset'
        ]
        self.data = dict.fromkeys(keys)
        self.main()
        
    def teams(self):
        teams_raw = self.game_soup.findAll('div', {'class': 'team-header', 'class': 'city'})
        team_keys = ['away_team', 'home_team']
        self.teams = {key: team_raw.contents[0] for key, team_raw in zip(team_keys, teams_raw)}
        self.data.update(self.teams)
        return(self.teams)
        
    def spread(self):
        spreads_raw = self.game_soup.findAll('div', {'class': 'value'})        
        spreads_list = [float(spread.contents[0]) for spread in spreads_raw]
        underdog_idx = [i for i,spread in enumerate(self.spreads) if spread > 0][0]
        spreads = {
            'underdog' : list(self.teams.values())[underdog_idx]
            'spread'   : spreads_list[underdog_idx]
        }
        self.data.update(spreads)
        return(spreads)
        
    def status(self):
        self.status_flag = self.game_soup.find('div', {'class' : 'status'}).contents[0]
        if status_flag == 'final':
            status = {'status': status_flag}
        else:
            status = {'status': 'pregame'}
        self.data.update(status)
        return(status)
    
    def score(self):
        score_raw = self.game_soup.findAll('td', {'class' : 'segment'})
        score = {
            'away_score' : int(scores_raw[4].contents[0]),
            'home_score' : int(scores_raw[9].contents[0])
        }
        self.data.update(score)
        
    def main(self):
        self.teams()
        self.spread()
        self.status()
        if self.status_flag == 'final':
            self.score()

class ProcessGamesToS3():
    def __init__(self, soup, week_id):
        self.soup = soup
        self.week_id = week_id
        games_pre = self.soup.findAll("div", {"class": "matchup pre"})
        games_final = self.soup.findAll("div", {"class": "matchup final"})
        self.games_soup = games_pre + games_final
        self.main()

    def write_s3(self, dictionary, filepath):
        s3 = boto3.resource('s3')
        s3object = s3.Object('atthletics', filepath)
        s3object.put(
            Body = (bytes(json.dumps(dictionary, indent=4).encode('UTF-8')))
        )        
        
    def main(self):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")        
        self.games = []
        for game_soup in self.games_soup:
            game_obj = Game(game_soup)
            self.games.append(game_obj.data)
        fp_params = {'week_id' : self.week_id, 'ts' : ts}
        s3_fp = 'data/os/week_id={week_id}/{ts}.json'.format(**fp_params)
        self.write_s3(self.games, s3_fp)
            
