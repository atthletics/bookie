from webdriver_wrapper import WebDriverWrapper
from bets.espn import espn_spreads
from bets.oddsshark import os_spreads

def lambda_handler(*args, **kwargs):
    #ESPN
    driver = WebDriverWrapper()
    driver.get_url('http://www.espn.com/college-football/scoreboard/_/group/80/year/2019/seasontype/2/week/1')
    driver.get_soup()
    espn_spreads.Parse(driver.soup)
    driver.close()

    #Oddsshark
    driver = WebDriverWrapper()
    driver.get_url('https://www.oddsshark.com/ncaaf/scores')
    driver.get_soup()
    os_spreads.Parse(driver.soup)
    driver.close()
