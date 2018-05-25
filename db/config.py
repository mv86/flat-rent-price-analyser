"""Setup database configuration"""
from configparser import ConfigParser
import pathlib


def db_config():
    """Returns dictionary with database connection configuration"""
    config_file = pathlib.Path.cwd() / 'database.ini'
    section = 'postgresql'
    parser = ConfigParser()
    parser.read(config_file)
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(
            f'Section {section} not found in the {config_file} file!'
        )
    return db_params
