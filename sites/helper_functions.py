"""Helper functions for sites package."""
import re

from logger import LOG


def valid_data(flat_info):
    """Check if extracted flat info valid. Return boolean."""
    valid = True
    description, postcode_area, bedrooms, price, website = flat_info
    if not description:
        LOG.warning(f'No description found: {website}. Skipping div')
        valid = False
    if postcode_area not in ('EH6', 'EH7', ''):
        LOG.info(f'{postcode_area} not a valid postcode: {website}. Skipping div')
        valid = False
    if bedrooms <= 0:
        LOG.warning(f'{bedrooms} not a valid num of bedrooms: {website}. Skipping div')
        valid = False
    if price <= 0:
        LOG.warning(f'{price} not a valid price: {website}. Skipping div')
        valid = False
    return valid


def extract_postcode_area(description):
    """Extract first three postcode chars (i.e EH7) from description. Return str, '' if none found."""
    postcode_search = re.search(r'[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def extract_num_of_bedrooms(description):
    """Extract the number of bedrooms from description. Return int, 0 if none found."""
    bedroom_search = re.search(r'\d bedroom', description)
    bedroom_descr = bedroom_search.group()
    if bedroom_descr:
        bedrooms = bedroom_descr[0]
        return int(bedrooms)
    return 0


def extract_price(price_string):
    """Extract flat price from string. Return int, 0 if none found."""
    raw_price = re.search(r'\d+(,\d+)?(.\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
        if '.' in price:
            price, _ = price.split('.')
        return int(price)
    return 0
