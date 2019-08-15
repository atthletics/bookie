import os
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

os.system("phantomjs scrape_espn.js")

soup = BeautifulSoup(open("espn.html"), "html.parser")
games = soup.findAll("article", {"class": "scoreboard football pregame js-show"})

for game in games:
    print(game.findAll("th", {"class": "line"}).getText())
    print(game.findAll("th", {"class": "date-time", "data-behavior": "date_time"}).getText())
