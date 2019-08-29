import os, yaml
from webdriver_wrapper import WebDriverWrapper
import espn_spreads
import os_spreads
fp = os.path.dirname(os.path.realpath(__file__))

def lambda_handler(*args, **kwargs):
    with open(fp + '/config.yaml', 'r') as f:
        config = yaml.load(f)

    #ESPN
    driver = WebDriverWrapper()
    driver.get_url(config['url1'])
    driver.get_soup()
    espn_spreads.Parse(driver.soup)
    driver.close()

    #Oddsshark
    driver = WebDriverWrapper()
    driver.get_url(config['url2'])
    driver.get_soup()
    os_spreads.Parse(driver.soup)
    driver.close()
