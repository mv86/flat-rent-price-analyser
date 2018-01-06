import logging, re, requests
from bs4 import BeautifulSoup


def find_flats_s1homes():
    s1homes_url = ('http://www.s1homes.com/rent/search/forrent_search_results.cgi?'
                   '&bedrooms=2-2'
                   '&bedroomsMin=2'
                   '&bedroomsMax=2'
                   '&type=Flat'
                   '&whenpropadded='
                   '&keywords=leith')

    r = requests.get(s1homes_url)
    if r.status_code < 400:
        if r.status_code != 200:
            logging.info(f'Status code = {r.status_code}')
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find_all('div', class_='row listing ')
            listings = []
            for div in divs:
                try:
                    description = get_description(div)
                    price = get_price(div)
                    listings.append((description, price))
                except Exception as e:
                    logging.error(f'Error in div loop: {e}')
            return listings
        except Exception as e:
            logging.error(f'Error in soup parsing: {e}')
            return []
    else:
        logging.error(f'Error code = {r.status_code}')
        return []


def get_description(html_div):
    h5 = html_div.find_all('h5')
    description_and_availabilty = h5[1].text.strip()
    description, _ = description_and_availabilty.split(',')
    address = html_div.h4.text.strip()
    full_description = f'{description}; {address}'
    return full_description


def get_price(html_div):
    h5 = html_div.find_all('h5')
    price_string = h5[0].text.strip()
    raw_price = re.search('\d+(,\d+)?', price_string)
    price = raw_price.group().replace(',', '')
    return int(price)
