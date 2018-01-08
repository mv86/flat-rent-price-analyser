#!/home/max/Python/projects/gumtree_scraper/venv/bin/python
import db.connect
from s1homes import find_flats_s1homes
from rightmove import find_flats_rightmove
from lettingweb import find_flats_lettingweb


def main():
    insert_daily_data()
    select_all_data()


def insert_daily_data():
    rightmove_flats = find_flats_rightmove()
    s1homes_flats = find_flats_s1homes()
    lettingweb_flats = find_flats_lettingweb()
    all_flats = rightmove_flats + s1homes_flats + lettingweb_flats
    sql = '''INSERT INTO flat_price_analysis
             (description, postcode_area, price, website)
             VALUES (%s, %s, %s, %s);'''
    for flat_info in all_flats:
        db.connect.insert(sql, flat_info)


def select_all_data():
    sql = 'SELECT * FROM flat_price_analysis;'
    flat_price_analysis_rows = db.connect.select(sql, ())
    filename = '/home/max/Python/projects/gumtree_scraper/table_data.txt'
    with open(filename, 'a') as f:
        for row in flat_price_analysis_rows:
            line_row = f'{str(row)}\n'
            f.write(line_row)


if __name__ == '__main__':
    main()
