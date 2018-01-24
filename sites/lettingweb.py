"""Scrape weekly flat rental prices from www.lettingweb.com for flats in Leith, Edinburgh """
from logger import LOG
from .helper_functions import (
    valid_data, extract_postcode_area, extract_num_of_bedrooms, extract_price
) 

# https://www.lettingweb.com/flats-to-rent/leith?&Term=Leith&BedsMin=1&BedsMax=2&HasPhotos=false&Added=LastWeek

URL = ('https://www.lettingweb.com/flats-to-rent/leith?'
       '&Term=Leith'
       '&BedsMin=1&BedsMax=2'
       '&HasPhotos=false'
       '&Added=LastWeek')  # LastWeek LastDay \xa0


def parse(soup):
    """Return a list of tuples containing flat listings from lettingweb url.

       Tuple = (description, postcode_area, price, website_name).
       
       Return empty list if no data found.
    """
    listings = []
    divs = soup.find_all('div', class_='panel')  # 'prop_info
    # Infomation is repeated in these divs. Only take the even iterations.
    wanted_divs = [div for idx, div in enumerate(divs) if idx % 2 != 0]
    for div in wanted_divs:
        try:
            flat_info = extract_flat_info(div)
            if not valid_data(flat_info): 
                continue
            listings.append(flat_info)
        except Exception as exception:
            LOG.error(f'Error in div loop: {exception}')
            continue
    return listings


def extract_flat_info(html_div):
    """Extract flat details and return a tuple.

       Tuple = (description, postcode_area, bedrooms, price, website_name)
    """
    description = html_div.find('h2', itemprop='description').text.strip()
    address = html_div.find('h2', itemprop='name').text.strip()
    # Remove excesive internal whitespace from address
    address = " ".join(address.split())
    full_description = f'{description}; {address}'

    postcode_area = extract_postcode_area(full_description)

    bedrooms = extract_num_of_bedrooms(full_description)

    price_string = html_div.find('h2', itemprop='offers').text.strip()
    price = extract_price(price_string)

    flat_info = (full_description, postcode_area, bedrooms, price, 'lettingweb')
    return flat_info
