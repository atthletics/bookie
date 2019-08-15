import urllib.request
import time
with urllib.request.urlopen('https://www.espn.com/college-football/scoreboard/_/group/80/year/2019/seasontype/2/week/1') as response:
   time.sleep(10)
   html = response.read()

with open('espn_test.html', 'wb') as f:
    f.write(html)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html)
parsed_html.body.find('<script>window.espn.scoreboardData').text

import re
test = re.search('<script>window.espn.scoreboardData(.*)</script>', html_str)


import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.espn.com/college-football/scoreboard/_/group/80/year/2019/seasontype/2/week/1')
time.sleep(10)
soup = BeautifulSoup(page.text, 'html.parser')

with open("espn_test.html", "w") as file:
    file.write(str(soup))


soup.findAll("th", {"class": "line"})
soup.findAll("a", {"class": "mobileScoreboardLink"})
