"""Scrape weekly flat rental prices from www.rightmove.co.uk for flats in Leith, Edinburgh."""
from logger import LOG
from .helper_functions import (
    valid_data, extract_postcode_area, extract_num_of_bedrooms, extract_price
)

# http://www.rightmove.co.uk/property-to-rent/find.html/?searchType=RENT&locationIdentifier=REGION%5E66954&insId=1&radius=0.0&minBedrooms=1&maxBedrooms=2&maxDaysSinceAdded=7&houseFlatShare=false

URL = ('http://www.rightmove.co.uk/property-to-rent/find.html/'
       '?searchType=RENT'
       '&locationIdentifier=REGION%5E66954&insId=1&radius=0.0'
       '&minBedrooms=1&maxBedrooms=2'
       '&maxDaysSinceAdded=7'  # 7 1
       '&houseFlatShare=false')


def parse(soup):
    """Return a list of tuples containing flat listings from rightmove url.

       Tuple = (description, postcode_area, bedrooms, price, website_name).

       Return empty list if no data found.
    """
    listings = []
    divs = soup.find_all('div', class_='is-list')  # replaced 'l-searchResult'
    wanted_divs = [div for div in divs if 'is-hidden' not in div.attrs['class']]
    for div in wanted_divs:
        try:
            flat_info = extract_flat_info(div)
            if not valid_data(flat_info): 
                continue
            listings.append(flat_info)
        except Exception as exception:
            LOG.error(f'Error: {exception}')
            continue
    return listings


def extract_flat_info(html_div):
    """Extract flat details and return a tuple.
    
       Tuple = (description, postcode_area, bedrooms, price, website_name).
    """
    description = html_div.find('h2', class_='propertyCard-title').text.strip()
    address = html_div.find('address', class_='propertyCard-address').span.text.strip()
    full_description = f'{description}: {address}'

    postcode_area = extract_postcode_area(full_description)

    bedrooms = extract_num_of_bedrooms(full_description) 

    price_string = html_div.find('span', class_='propertyCard-priceValue').text.strip()
    price = extract_price(price_string)

    flat_info = (full_description, postcode_area, bedrooms, price, 'rightmove')
    return flat_info
