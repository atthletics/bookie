from datetime import datetime
from webdriver_wrapper import WebDriverWrapper
from bets.espn import spreads

def get_url(self):
    today = datetime.today()

def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()
    driver.get_url('http://www.espn.com/college-football/scoreboard/_/group/80/year/2019/seasontype/2/week/1')
    driver.get_soup()
    spreads.Parse(driver.soup)

    driver.close()
