"""Scrapes weekly flat rental prices from www.s1homes.com for flats in Leith, Edinburgh."""
from logger import LOG
from .helper_functions import get_postcode_area, get_num_of_bedrooms, get_price 

# http://www.s1homes.com/rent/search/forrent_search_results.cgi?&bedrooms=1-2&bedroomsMin=1&bedroomsMax=2&type=Flat&whenpropadded=7&keywords=leith

URL = ('http://www.s1homes.com/rent/search/forrent_search_results.cgi?'
       '&bedrooms=1-2'
       '&bedroomsMin=1'
       '&bedroomsMax=2'
       '&type=Flat'
       '&whenpropadded=7'  # 1
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
            listings.append((description, postcode_area, bedrooms, price, 's1homes'))
        except Exception as exception:
            LOG.error(f'Error in div loop: {exception}')
            continue
    return listings


def extract_flat_info(html_div):
    """Extracts flat details and returns as variables"""
    p_tags = html_div.find_all('p')

    description_and_availabilty = p_tags[1].text.strip()
    description, _ = description_and_availabilty.split(',')
    address = html_div.h4.text.strip()
    full_description = f'{description}; {address}'

    postcode_area = get_postcode_area(description)

    bedrooms = get_num_of_bedrooms(description)

    price_string = p_tags[0].text.strip()
    price = get_price(price_string)

    return full_description, postcode_area, bedrooms, price
