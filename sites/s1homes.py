"""Scrapes weekly flat rental prices from www.s1homes.com for flats in Leith, Edinburgh."""
from logger import LOG
from .helper_functions import (
    valid_data, extract_postcode_area, extract_num_of_bedrooms, extract_price
)

# http://www.s1homes.com/rent/search/forrent_search_results.cgi?&bedrooms=1-2&bedroomsMin=1&bedroomsMax=2&type=Flat&whenpropadded=7&keywords=leith

URL = ('http://www.s1homes.com/rent/search/forrent_search_results.cgi?'
       '&bedrooms=1-2'
       '&bedroomsMin=1'
       '&bedroomsMax=2'
       '&type=Flat'
       '&whenpropadded='  # 7 1
       '&keywords=leith')


def parse(soup):
    """Returns a list of tuples containing flat listings from s1homes url.
       Tuple = (description, postcode_area, bedrooms, price, website_name).
       Returns an empty list if no data found.
    """
    listings = []
    divs = soup.find_all('div', class_='row listing ')
    for div in divs:
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
    """Extracts flat details and returns a tuple.
       Tuple = (description, postcode_area, bedrooms, price, website_name)
    """
    p_tags = html_div.find_all('p')

    description_and_availabilty = p_tags[1].text.strip()
    description, _ = description_and_availabilty.split(',')
    address = html_div.h4.text.strip()
    full_description = f'{description}; {address}'

    postcode_area = extract_postcode_area(full_description)

    bedrooms = extract_num_of_bedrooms(full_description)

    price_string = p_tags[0].text.strip()
    price = extract_price(price_string)

    flat_info = (full_description, postcode_area, bedrooms, price, 's1homes')
    return flat_info
