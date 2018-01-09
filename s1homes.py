import re, requests
from bs4 import BeautifulSoup
from logger import logger

# http://www.s1homes.com/rent/search/forrent_search_results.cgi?&bedrooms=2-2&bedroomsMin=2&bedroomsMax=2&type=Flat&whenpropadded=1&keywords=leith


def find_flats_s1homes():
    s1homes_url = ('http://www.s1homes.com/rent/search/forrent_search_results.cgi?'
                   '&bedrooms=2-2'
                   '&bedroomsMin=2'
                   '&bedroomsMax=2'
                   '&type=Flat'
                   '&whenpropadded='  # 1
                   '&keywords=leith')

    r = requests.get(s1homes_url)
    if r.status_code < 400:
        if r.status_code != 200:
            logger.warning(f'Status code = {r.status_code}')
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find_all('div', class_='row listing ')
            listings = []
            for div in divs:
                try:
                    description = get_description(div)
                    postcode_area = get_postcode_area(description)
                    price = get_price(div)
                    listings.append((description, postcode_area, price, 's1homes'))
                except Exception as e:
                    logger.error(f'Error in div loop: {e}')
                    continue
            return listings
        except Exception as e:
            logger.error(f'Error in soup parsing: {e}')
            return []
    else:
        logger.error(f'Error code = {r.status_code}')
        return []


def get_description(html_div):
    h5 = html_div.find_all('h5')
    description_and_availabilty = h5[1].text.strip()
    description, _ = description_and_availabilty.split(',')
    address = html_div.h4.text.strip()
    full_description = f'{description}; {address}'
    return full_description


def get_postcode_area(description):
    postcode_search = re.search('[A-Z][A-Z]\d+', description)
    if postcode_search:
        postcode_area = postcode_search.group()
    else:
        postcode_area = ''
    return postcode_area


def get_price(html_div):
    h5 = html_div.find_all('h5')
    price_string = h5[0].text.strip()
    raw_price = re.search('\d+(,\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
    else:
        price = 0
    return int(price)
