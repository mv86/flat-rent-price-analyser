#!/home/max/Python/projects/flat_price_analyser/venv/bin/python
"""Script to scrape data from flat listing websites and store in db. Runs weekly."""
from pathlib import Path

from tabulate import tabulate

import db.connect
from sites import scraper


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
    # Convert to list of lists for tabulate function
    rows = [list(row) for row in flat_price_analysis_rows]
    headers = (
        ['ID', 'Description', 'Postcode Area', 'Bedrooms', 'Price', 'Listed On', 'Date Inserted']
    )
    table = tabulate(rows, headers, tablefmt='psql', numalign='left')

    file_path = Path.cwd() / 'table_data.txt'
    with open(file_path, 'w') as file:
        file.write(table)


def main():
    """Entry point to script."""
    # Main script functionality
    insert_weekly_data()
    # Create table_data file after every data insert for developing/debugging purposes
    select_all_data()


if __name__ == '__main__':
    main()
