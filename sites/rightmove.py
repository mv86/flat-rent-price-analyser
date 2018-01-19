"""Scrapes weekly flat rental prices from www.rightmove.co.uk for flats in Leith, Edinburgh."""
from logger import LOG
from .helper_functions import get_postcode_area, get_num_of_bedrooms, get_price

# http://www.rightmove.co.uk/property-to-rent/find.html/?searchType=RENT&locationIdentifier=REGION%5E66954&insId=1&radius=0.0&minBedrooms=1&maxBedrooms=2&maxDaysSinceAdded=1&houseFlatShare=false

URL = ('http://www.rightmove.co.uk/property-to-rent/find.html/'
       '?searchType=RENT'
       '&locationIdentifier=REGION%5E66954&insId=1&radius=0.0'
       '&minBedrooms=1&maxBedrooms=2'
       '&maxDaysSinceAdded=7'  # 1
       '&houseFlatShare=false')


def parse(soup):
    """Returns a list of tuples containing flat listings from rightmove url.
       Tuple = (description, postcode_area, bedrooms, price, website_name).
       Returns an empty list if no data found.
    """
    listings = []
    divs = soup.find_all('div', class_='is-list')  # replaced 'l-searchResult'
    wanted_divs = [div for div in divs if 'is-hidden' not in div.attrs['class']]
    for div in wanted_divs:
        try:
            description, postcode_area, bedrooms, price = extract_flat_info(div) 
            if not description:
                LOG.warning('No description found. Skipping div')
                continue
            if bedrooms <= 0:
                LOG.warning(f'Invalid num of bedrooms: {bedrooms}. Skipping div')
                continue
            if price <= 0:
                LOG.warning(f'{price} not a valid price. Skipping div')
                continue
            listings.append((description, postcode_area, bedrooms, price, 'rightmove'))
        except Exception as exception:
            LOG.error(f'Error: {exception}')
            continue
    return listings


def extract_flat_info(html_div):
    """Extracts flat details and returns as variables"""
    property_type = html_div.find('h2', class_='propertyCard-title').text.strip()
    address = html_div.find('address', class_='propertyCard-address').span.text.strip()
    description = f'{property_type}: {address}'

    postcode_area = get_postcode_area(description)

    bedrooms = get_num_of_bedrooms(description) 

    price_string = html_div.find('span', class_='propertyCard-priceValue').text.strip()
    price = get_price(price_string)

    return description, postcode_area, bedrooms, price
