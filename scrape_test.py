import logging
from rightmove import find_flats_rightmove
from s1homes import find_flats_s1homes
from lettingweb import find_flats_lettingweb


logging.basicConfig(level=logging.INFO,
                    filename='scraper_logs.log',
                    format='%(levelname)s:%(asctime)s:%(funcName)s:%(message)s',
                    datefmt='%d-%m-%Y')

log = logging.getLogger()


def main():
    rightmove_flats = find_flats_rightmove()
    s1homes_flats = find_flats_s1homes()
    lettingweb_flats = find_flats_lettingweb()


if __name__ == '__main__':
    main()
