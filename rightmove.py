import re, requests
from bs4 import BeautifulSoup
from logger import logger

# http://www.rightmove.co.uk/property-to-rent/find.html/?searchType=RENT&locationIdentifier=REGION%5E66954&insId=1&radius=0.0&minBedrooms=2&maxBedrooms=2&maxDaysSinceAdded=1&houseFlatShare=false


def find_flats_rightmove():
    rightmove_url = ('http://www.rightmove.co.uk/property-to-rent/find.html/'
                     '?searchType=RENT'
                     '&locationIdentifier=REGION%5E66954&insId=1&radius=0.0'
                     '&minBedrooms=2&maxBedrooms=2'
                     '&maxDaysSinceAdded=1'
                     '&houseFlatShare=false')

    r = requests.get(rightmove_url)
    if r.status_code < 400:
        if r.status_code != 200:
            logger.warning(f'Status code = {r.status_code}')
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find_all('div', class_='is-list')  # replaced 'l-searchResult'
            listings = []
            for div in divs:
                try:
                    description = get_description(div)
                    price = get_price(div)
                    if price > 0:
                        listings.append((description, price))
                    else:
                        # TODO Does this log the same ammount of errors every day?
                        logger.error(f'Description: {description}, Price: {price}.')
                except Exception as e:
                    logger.error(f'Error: {e}')
                    return []
            return listings
        except Exception as e:
            logger.error(f'Error: {e}')
            return []
    else:
        logger.error(f'Error code = {r.status_code}')
        return []


def get_description(html_div):
    property_type = html_div.find('h2', class_='propertyCard-title').text.strip()
    address = html_div.find('address', class_='propertyCard-address').span.text.strip()
    description = f'{property_type}: {address}'
    return description


def get_price(html_div):
    price_and_month = html_div.find('span', class_='propertyCard-priceValue').text.strip()
    # String has pcm letters with price i.e. 999.00 pcm. Use regex to select only price
    price = extract_price(price_and_month)
    return price


def extract_price(original_string):
    price = re.search('\d+(,\d+)?(.\d+)?', original_string)
    if not price:
        return 0
    else:
        try:
            price = price.group().replace(',', '')
            # Remove decimal place and pence
            if '.' in price:
                price, _ = price.split('.')
            return int(price)
        except Exception as e:
            logger.error(f'Error: {e}')
            return 0
