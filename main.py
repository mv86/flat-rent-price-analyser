#!/home/max/Python/projects/flat_price_analyser/venv/bin/python
"""Script to scrape data from flat listing websites and store in db. Runs weekly."""
from prettytable import PrettyTable
import db.connect
import scraper

def insert_weekly_data():
    """Scrape flat listing data using scraper module and insert into db"""
    listings = scraper.scrape_all_sites()
    sql = '''INSERT INTO flat_price_analysis
             (description, postcode_area, bedrooms, price, website)
             VALUES (%s, %s, %s, %s, %s);'''
    db.connect.insert(sql, listings)


def select_all_data():
    """Insert all current data from flat_price_analysis table into table_data file"""
    sql = 'SELECT * FROM flat_price_analysis;'
    flat_price_analysis_rows = db.connect.select(sql)
    file_path = '/home/max/Python/projects/flat_price_analyser/table_data.txt'
    headers = (
        ['ID', 'Description', 'Postcode Area', 'Bedrooms', 'Price', 'Listed On', 'Date Inserted']
    )
    table = PrettyTable(headers)
    for row in flat_price_analysis_rows:
        row_info = []
        for item in row:
            row_info.append(str(item))
        table.add_row(row_info)
    with open(file_path, 'w') as file:
        file.write(str(table))


def main():
    """Entry point to script."""
    insert_weekly_data()
    select_all_data()


if __name__ == '__main__':
    main()
