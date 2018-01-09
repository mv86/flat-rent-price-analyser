import re, requests
from bs4 import BeautifulSoup
from logger import logger

# https://www.lettingweb.com/flats-to-rent/leith?&Term=Leith&BedsMin=2&BedsMax=2&HasPhotos=false&Added=LastDay


def find_flats_lettingweb():
    lettingweb_url = ('https://www.lettingweb.com/flats-to-rent/leith?'
                      '&Term=Leith'
                      '&BedsMin=2&BedsMax=2'
                      '&HasPhotos=false'
                      '&Added=')  # LastDay

    r = requests.get(lettingweb_url)
    if r.status_code < 400:
        if r.status_code != 200:
            logger.warning(f'Status code = {r.status_code}')
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find_all('div', class_='panel')  # 'prop_info
            listings = []
            # Infomation is repeated in these divs. Only take the even iterations.
            i = 1
            for div in divs:
                if i % 2 == 0:
                    i += 1
                    try:
                        description = get_description(div)
                        postcode_area = get_postcode_area(description)
                        price = get_price(div)
                        listings.append((description, postcode_area, price, 'lettingweb'))
                    except Exception as e:
                        logger.error(f'Error in div loop: {e}')
                        continue
                else:
                    i += 1
            return listings
        except Exception as e:
            logger.error(f'Error in soup parsing: {e}')
            return []
    else:
        logger.error(f'Error code = {r.status_code}')
        return []


def get_description(html_div):
    address = html_div.find('h2', itemprop='name').text.strip()
    raw_description = html_div.find('h2', itemprop='description').text.strip()
    description, _ = raw_description.split('\xa0')
    description = description.strip()
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
    price_string = html_div.find('h2', itemprop='offers').text.strip()
    raw_price = re.search('\d+(,\d+)?', price_string)
    if raw_price:
        price = raw_price.group().replace(',', '')
    else:
        price = 0
    return int(price)
