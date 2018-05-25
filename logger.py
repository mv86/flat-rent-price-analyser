"""Create logger settings for project"""
import logging
import pathlib


def config_logger():
    """Create project-wide logger, define settings and return logger"""
    file_path = pathlib.Path.cwd() / 'scraper_logs.log'
    logging_format = '%(levelname)s:%(asctime)s:%(module)s:%(funcName)s:%(message)s'
    logging.basicConfig(level=logging.INFO,
                        filename=file_path,
                        format=logging_format,
                        datefmt='%d-%m-%Y')
    logger = logging.getLogger(__name__)
    return logger

LOG = config_logger()
