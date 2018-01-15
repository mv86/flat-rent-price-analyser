"""Creates logger settings for project"""
import logging


def config_logger():
    """Creates project-wide logger, defines settings and returns"""
    file_path = '/home/max/Python/projects/flat_price_analyser/scraper_logs.log'
    logging_format = '%(levelname)s:%(asctime)s:%(funcName)s:%(message)s'
    logging.basicConfig(level=logging.WARNING,
                        filename=file_path,
                        format=logging_format,
                        datefmt='%d-%m-%Y')
    logger = logging.getLogger(__name__)
    return logger

LOG = config_logger()
