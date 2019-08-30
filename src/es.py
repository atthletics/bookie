import json, time
from bs4 import BeautifulSoup
import boto3

class Game():
    def __init__(self, game_soup):
        self.game_soup = game_soup
        keys = [
            'game_status',
            'game_ts',
            'game_id',
            'away_team_id',
            'home_team_id',
            'underdog_id', 
            'spread',
            'away_score',
            'home_score',
            'winner',
            'is_upset'
        ]
        self.data = dict.fromkeys(keys)
        self.main()

    def game(self):
        game_id = {'game_id' : self.game_soup.attrs['id']}
        self.data.update(game_id)
        short_names = self.game_soup.findAll('span', {'class': 'sb-team-abbrev'})
        self.short_names = [elem.contents[0] for elem in short_names]
        self.short_names_str = ' at '.join(self.short_names)
        return(self.short_names_str)
            
    def teams(self):
        teams_raw = [
            self.game_soup.attrs['data-awayid'],
            self.game_soup.attrs['data-homeid']
        ]
        team_keys = ['away_team_id', 'home_team_id']
        self.team_ids = {key: team_raw for key, team_raw in zip(team_keys, teams_raw)}
        self.data.update(self.team_ids)
        return(self.team_ids)

    def spread(self):
        spread_raw = self.game_soup.find('th', {'class': 'line'}).contents[0]
        spread_split = str.split(spread_raw, ' ')
        favorite = spread_split[0]
        favorite_id = self.short_names.index(favorite)
        underdog_idx = abs(favorite_id - 1)
        spreads = {
            'underdog' : list(self.team_ids.values())[underdog_idx],
            'spread'   : abs(float(spread_split[1]))
        }
        self.data.update(spreads)
    
    def main(self):
        self.game()
        self.teams()
        self.spread()

class ProcessGamesToS3():
    def __init__(self, soup, week_id):
        self.soup = soup
        self.week_id = week_id
        self.games_soup = self.soup.findAll("article",
            {"class": "scoreboard football pregame js-show"})
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
            try:
                game_obj = Game(game_soup)
                print('Processing: ' + game_obj.short_names_str)
                self.games.append(game_obj.data)
            except AttributeError:
                print('ERROR: ' + game_obj.short_names_str)
        fp_params = {'week_id' : self.week_id, 'ts' : ts}
        s3_fp = 'data/es/week_id={week_id}/{ts}.json'.format(**fp_params)
        self.write_s3(self.games, s3_fp)
 
