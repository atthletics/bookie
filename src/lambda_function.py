import os, yaml
from webdriver_wrapper import WebDriverWrapper
import es_data
import os_data
fp = os.path.dirname(os.path.realpath(__file__))

def lambda_handler(*args, **kwargs):
    with open(fp + '/config.yaml', 'r') as f:
        config = yaml.load(f)

    driver = WebDriverWrapper()
    driver.get_url(config['url1'])
    driver.get_soup()
    es_data.ProcessGamesToS3(driver.soup, 1)
    driver.close()

    driver = WebDriverWrapper()
    driver.get_url(config['url2'])
    driver.get_soup()
    os_data.ProcessGamesToS3(driver.soup, 1)
    driver.close()
