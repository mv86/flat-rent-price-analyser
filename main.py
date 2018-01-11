#!/home/max/Python/projects/flat_price_analyser/venv/bin/python
import db.connect
from prettytable import PrettyTable
from scrapers import rightmove, s1homes, lettingweb


def main():
    insert_daily_data()
    select_all_data()


def insert_daily_data():
    rightmove_info = rightmove.scrape()
    s1homes_info = s1homes.scrape()
    lettingweb_info = lettingweb.scrape()
    all_info = rightmove_info + s1homes_info + lettingweb_info
    sql = '''INSERT INTO flat_price_analysis
             (description, postcode_area, price, website)
             VALUES (%s, %s, %s, %s);'''
    for flat_info in all_info:
        db.connect.insert(sql, flat_info)


def select_all_data():
    # TODO Format data properly into file
    sql = 'SELECT * FROM flat_price_analysis;'
    flat_price_analysis_rows = db.connect.select(sql, ())
    file = '/home/max/Python/projects/flat_price_analyser/table_data.txt'
    headers = ['ID', 'Description', 'Postcode Area', 'Price', 'Listed On', 'Date Inserted']
    table = PrettyTable(headers)
    for row in flat_price_analysis_rows:
        row_info = []
        for item in row:
            row_info.append(str(item))
        table.add_row(row_info)
    with open(file, 'w') as f:
            f.write(str(table))


if __name__ == '__main__':
    main()
