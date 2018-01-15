"""Scrapes weekly flat rental prices from www.lettingweb.com for flats in Leith, Edinburgh """
import re
import requests
from bs4 import BeautifulSoup
from logger import LOG

# https://www.lettingweb.com/flats-to-rent/leith?&Term=Leith&BedsMin=2&BedsMax=2&HasPhotos=false&Added=LastDay


def scrape():
    """Returns a list of tuples containing flat listings from s1homes url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found or Exception raised.
    """
    lettingweb_url = ('https://www.lettingweb.com/flats-to-rent/leith?'
                      '&Term=Leith'
                      '&BedsMin=2&BedsMax=2'
                      '&HasPhotos=false'
                      '&Added=LastWeek')  # LastDay

    request = requests.get(lettingweb_url)
    if request.status_code <= 400:
        LOG.error(f'Error code = {request.status_code}')
        return []
    else:
        if request.status_code != 200:
            LOG.warning(f'Status code = {request.status_code}')
        try:
            listings = parse(request)
            return listings
        except Exception as exception:
            LOG.error(f'Error in soup parsing: {exception}')
            return []


def parse(request):
    """Helper function for scrape().
       Returns a list of tuples containing flat listings from lettingweb url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found.
    """
    soup = BeautifulSoup(request.text, 'html.parser')
    divs = soup.find_all('div', class_='panel')  # 'prop_info
    listings = []
    # Infomation is repeated in these divs. Only take the even iterations.
    i = 1
    for div in divs:
        if i % 2 == 0:
            i += 1
            try:
                description = get_description(div)
                postcode_area = get_postcode_area(description)
                price = get_price(div)
                if price <= 0:
                    LOG.warning(f'{price} not a valid price. Skipping div')
                    continue
                listings.append((description, postcode_area, price, 'lettingweb'))
            except Exception as exception:
                LOG.error(f'Error in div loop: {exception}')
                continue
        else:
            i += 1
    return listings


def get_description(html_div):
    """Extracts flat details and return str with description and address"""
    address = html_div.find('h2', itemprop='name').text.strip()
    raw_description = html_div.find('h2', itemprop='description').text.strip()
    # TODO description occasionaly has extra info, remove this
    description, _ = raw_description.split('\xa0')
    description = description.strip()
    full_description = f'{description}; {address}'
    return full_description


def get_postcode_area(description):
    """Extracts first three postcode chars (i.e EH7) and returns as str"""
    postcode_search = re.search(r'[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def get_price(html_div):
    """Extracts flat price and returns as int"""
    price_string = html_div.find('h2', itemprop='offers').text.strip()
    raw_price = re.search(r'\d+(,\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
    else:
        price = 0
    return int(price)
