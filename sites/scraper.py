"""Scrape and parse websites. Link between main script and sites package"""
import requests
from bs4 import BeautifulSoup
from sites import lettingweb, rightmove, s1homes
from logger import LOG


def scrape_all_sites():
    """Scrape flat listing websites and parse into soup object.

       Pass to site parse function to extract listing infomation.
       
       Return list of listings. Return empty list if no listings found.
    """
    listings = []
    sites = [lettingweb, rightmove, s1homes]
    for site in sites:
        request = requests.get(site.URL)
        if request.status_code >= 400:
            LOG.error(f'{site} request error: Status code {request.status_code}.')
            continue
        else:
            try:
                soup = BeautifulSoup(request.text, 'lxml')
                listings.extend(site.parse(soup))
            except Exception as exception:
                LOG.error(f'{site} error when parsing soup: {exception}.')
                continue
    if not listings:
        LOG.info('No appropriate flat listings this week.')
    return listings 
