import logging

logging.basicConfig(level=logging.WARNING,
                    filename='/home/max/Python/projects/gumtree_scraper/scraper_logs.log',
                    format='%(levelname)s:%(asctime)s:%(funcName)s:%(message)s',
                    datefmt='%d-%m-%Y')

logger = logging.getLogger(__name__)
