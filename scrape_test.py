import logging
# import requests
# from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    filename='scraper_logs.log',
                    format='%(levelname)s:%(asctime)s:%(funcName)s:%(message)s',
                    datefmt='%d-%m-%Y')

log = logging.getLogger()
