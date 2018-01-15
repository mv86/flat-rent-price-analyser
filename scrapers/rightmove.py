"""Scrapes weekly flat rental prices from www.rightmove.co.uk for flats in Leith, Edinburgh."""
import re
import requests
from bs4 import BeautifulSoup
from logger import LOG

# http://www.rightmove.co.uk/property-to-rent/find.html/?searchType=RENT&locationIdentifier=REGION%5E66954&insId=1&radius=0.0&minBedrooms=2&maxBedrooms=2&maxDaysSinceAdded=1&houseFlatShare=false


def scrape():
    """Returns a list of tuples containing flat listings from s1homes url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found or Exception raised.
    """
    rightmove_url = ('http://www.rightmove.co.uk/property-to-rent/find.html/'
                     '?searchType=RENT'
                     '&locationIdentifier=REGION%5E66954&insId=1&radius=0.0'
                     '&minBedrooms=2&maxBedrooms=2'
                     '&maxDaysSinceAdded=7'  # 1
                     '&houseFlatShare=false')

    request = requests.get(rightmove_url)
    if request.status_code >= 400:
        LOG.error(f'Error code = {request.status_code}')
        return []
    else:
        if request.status_code != 200:
            LOG.warning(f'Status code = {request.status_code}')
        try:
            listings = parse(request)
            return listings
        except Exception as exception:
            LOG.error(f'Error: {exception}')
            return []


def parse(request):
    """Helper function for scrape().
       Returns a list of tuples containing flat listings from rightmove url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found.
    """
    soup = BeautifulSoup(request.text, 'html.parser')
    divs = soup.find_all('div', class_='is-list')  # replaced 'l-searchResult'
    wanted_divs = []
    for div in divs:
        if 'is-hidden' not in div.attrs['class']:
            wanted_divs.append(div)
    listings = []
    for div in wanted_divs:
        try:
            description = get_description(div)
            postcode_area = get_postcode_area(description)
            price = get_price(div)
            if not price > 0:
                LOG.warning(f'{price} not a valid price. Skipping div')
                continue
            listings.append((description, postcode_area, price, 'rightmove'))
        except Exception as exception:
            LOG.error(f'Error: {exception}')
            continue
    return listings


def get_description(html_div):
    """Extracts flat details and return str with description and address"""
    property_type = html_div.find('h2', class_='propertyCard-title').text.strip()
    address = html_div.find('address', class_='propertyCard-address').span.text.strip()
    description = f'{property_type}: {address}'
    return description


def get_postcode_area(description):
    """Extracts first three postcode chars (i.e. EH7) and returns as str"""
    postcode_search = re.search(r'[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def get_price(html_div):
    """Extracts flat price and returns as int"""
    price_and_month = html_div.find('span', class_='propertyCard-priceValue').text.strip()
    # String has pcm letters with price i.e. 999.00 pcm. Use regex to select only price
    price = extract_price(price_and_month)
    return price


def extract_price(original_string):
    """Helper funciton for get_price, extracts price from string and returns as int"""
    price = re.search(r'\d+(,\d+)?(.\d+)?', original_string)
    if price:
        price = price.group().replace(',', '')
        # Remove decimal place and pence
        if '.' in price:
            price, _ = price.split('.')
        return int(price)
    else:
        return 0
