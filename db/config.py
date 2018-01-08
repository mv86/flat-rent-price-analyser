from configparser import ConfigParser


ini_file = 'home/max/Python/projects/gumtree_scraper/db/database.ini'


def config(filename=ini_file, section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file!')
    return db
