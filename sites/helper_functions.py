"""Helper functions to help extract required infomation from parsed websites"""
import re


def get_postcode_area(description):
    """Extracts first three postcode chars (i.e EH7) and returns as str"""
    postcode_search = re.search(r'[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def get_num_of_bedrooms(description):
    """Extracts the number of bedrooms and returns as int"""
    bedroom_search = re.search(r'\d bedroom', description)
    bedroom_descr = bedroom_search.group()
    if bedroom_descr:
        bedrooms = bedroom_descr[0]
        return int(bedrooms)
    return 0


def get_price(price_string):
    """Extracts flat price and returns as int"""
    raw_price = re.search(r'\d+(,\d+)?(.\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
        if '.' in price:
            price, _ = price.split('.')
        return int(price)
    return 0
