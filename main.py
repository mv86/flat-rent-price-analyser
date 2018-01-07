#!usr/bin/python3
import db.connect
from s1homes import find_flats_s1homes
from rightmove import find_flats_rightmove
from lettingweb import find_flats_lettingweb


def main():
    rightmove_flats = find_flats_rightmove()
    s1homes_flats = find_flats_s1homes()
    lettingweb_flats = find_flats_lettingweb()
    all_flats = rightmove_flats + s1homes_flats + lettingweb_flats
    for flat_info in all_flats:
        sql = '''INSERT INTO flat_price_analysis (description, price)
                 VALUES (%s, %s);'''
        db.connect.insert(sql, flat_info)


if __name__ == '__main__':
    main()
