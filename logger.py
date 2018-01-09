import logging

log_file = '/home/max/Python/projects/flat_price_analyser/scraper_logs.log'
log_format = '%(levelname)s:%(asctime)s:%(funcName)s:%(message)s'

logging.basicConfig(level=logging.WARNING,
                    filename=log_file,
                    format=log_format,
                    datefmt='%d-%m-%Y')

logger = logging.getLogger(__name__)
