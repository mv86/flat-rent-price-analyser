"""Helper functions to help extract required infomation from parsed websites"""
import re
from logger import LOG


def valid_data(flat_info):
    """Check if extracted flat info valid, ignoring postcode_area & website. Returns boolean"""
    valid = True
    description, _, bedrooms, price, _ = flat_info
    if not description:
        LOG.warning('No description found. Skipping div')
        valid = False
    if bedrooms <= 0:
        LOG.warning(f'Invalid num of bedrooms: {bedrooms}. Skipping div')
        valid = False
    if price <= 0:
        LOG.warning(f'{price} not a valid price. Skipping div')
        valid = False
    return valid


def extract_postcode_area(description):
    """Extracts first three postcode chars (i.e EH7) and returns as str"""
    postcode_search = re.search(r'[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def extract_num_of_bedrooms(description):
    """Extracts the number of bedrooms and returns as int"""
    bedroom_search = re.search(r'\d bedroom', description)
    bedroom_descr = bedroom_search.group()
    if bedroom_descr:
        bedrooms = bedroom_descr[0]
        return int(bedrooms)
    return 0


def extract_price(price_string):
    """Extracts flat price and returns as int"""
    raw_price = re.search(r'\d+(,\d+)?(.\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
        if '.' in price:
            price, _ = price.split('.')
        return int(price)
    return 0
