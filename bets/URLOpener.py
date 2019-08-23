import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import logging as log
fp = os.path.dirname(os.path.realpath(__file__))
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class SeleniumHeadless():
    '''
    Gets BeautifulSoup object from inputted URL. Waits for the page to render
    first before parsing the HTML.
    '''
    def __init__(self):
        log.info('Initializing headless browser')
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def get_soup(self, url):
        log.info('Opening page for :' + url)
        self.browser.get(url)
        log.info('Parsing HTML')
        html = self.browser.page_source
        self.soup = BeautifulSoup(html, 'lxml')
        return(self.soup)
