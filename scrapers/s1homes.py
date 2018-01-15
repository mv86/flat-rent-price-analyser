"""Scrapes weekly flat rental prices from www.s1homes.com for flats in Leith, Edinburgh."""
import re 
import requests
from bs4 import BeautifulSoup
from logger import LOG

# http://www.s1homes.com/rent/search/forrent_search_results.cgi?&bedrooms=2-2&bedroomsMin=2&bedroomsMax=2&type=Flat&whenpropadded=1&keywords=leith


def scrape():
    """Returns a list of tuples containing flat listings from s1homes url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found or Exception raised.
    """
    s1homes_url = ('http://www.s1homes.com/rent/search/forrent_search_results.cgi?'
                   '&bedrooms=2-2'
                   '&bedroomsMin=2'
                   '&bedroomsMax=2'
                   '&type=Flat'
                   '&whenpropadded=7'  # 1
                   '&keywords=leith')

    request = requests.get(s1homes_url)
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
            LOG.error(f'Error in soup parsing: {exception}')
            return []
        

def parse(request):
    """Helper function for scrape().
       Returns a list of tuples containing flat listings from s1homes url.
       Tuple = (description, postcode_area, price, website_name).
       Returns an empty list if no data found.
    """
    soup = BeautifulSoup(request.text, 'html.parser')
    divs = soup.find_all('div', class_='row listing ')
    listings = []
    for div in divs:
        try:
            description = get_description(div)
            postcode_area = get_postcode_area(description)
            price = get_price(div)
            if price <= 0:
                LOG.warning(f'{price} not a valid price. Skipping div')
                continue
            listings.append((description, postcode_area, price, 's1homes'))
        except Exception as exception:
            LOG.error(f'Error in div loop: {exception}')
            continue
    return listings


def get_description(html_div):
    """Extracts flat details and return str with description and address"""
    h5_tags = html_div.find_all('h5')
    description_and_availabilty = h5_tags[1].text.strip()
    description, _ = description_and_availabilty.split(',')
    address = html_div.h4.text.strip()
    full_description = f'{description}; {address}'
    return full_description


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
    h5_tags = html_div.find_all('h5')
    price_string = h5_tags[0].text.strip()
    raw_price = re.search(r'\d+(,\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
    else:
        price = 0
    return int(price)
