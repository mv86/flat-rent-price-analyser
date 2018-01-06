import logging, re, requests
from bs4 import BeautifulSoup


# 'https://www.lettingweb.com/flats-to-rent/leith?&Term=Leith&BedsMin=2&BedsMax=2&HasPhotos=false&Added=LastDay'


def find_flats_lettingweb():
    lettingweb_url = ('https://www.lettingweb.com/flats-to-rent/leith?'
                      '&Term=Leith'
                      '&BedsMin=2&BedsMax=2'
                      '&HasPhotos=false'
                      '&Added=LastDay')

    r = requests.get(lettingweb_url)
    if r.status_code < 400:
        if r.status_code != 200:
            logging.info(f'Status code = {r.status_code}')
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find_all('div', class_='panel')
            listings = []
            # Infomation is repeated in these divs. Only take the even iterations.
            i = 1
            for div in divs:
                if i % 2 == 0:
                    try:
                        raw_description = div.find('h2', itemprop='description').text.strip()
                        description = raw_description.replace('\xa0', ' ')
                        price_string = div.find('h2', itemprop='offers').text.strip()
                        raw_price = re.search('\d+(,\d+)?', price_string)
                        price = raw_price.group().replace(',', '')
                        listings.append((description, int(price)))
                    except Exception as e:
                        logging.error(f'Error in div loop: {e}')
                        return []
                    i += 1
                else:
                    i += 1
            return listings
        except Exception as e:
            logging.error(f'Error in soup parsing: {e}')
            return []
    else:
        logging.error(f'Error code = {r.status_code}')
        return []
