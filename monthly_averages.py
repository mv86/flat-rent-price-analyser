import statistics
import db.connect


def calculate_median(month):
    if type(month) is not str:
        raise TypeError('String in required for month argument')
    month = month.lower()
    if month in month_dictionary:
        sql_month = month_dictionary[month]
    else:
        raise ValueError("Month argument needs to be a valid month in either format 'apr' or 'april'")
    sql = "SELECT price FROM flat_price_analysis WHERE date_part('month', created_on) = (%s);"
    monthly_flat_prices = db.connect.select(sql, (sql_month,))
    print(monthly_flat_prices)
    print()
    # file = '/home/max/Python/projects/flat_price_analyser/month_data.txt'
    # with open(file, 'w') as f:
    #         f.write(str(table))
    median_price = statistics.median(monthly_flat_prices[0])
    print(median_price)


month_dictionary = {
    'jan': 1,
    'january': 1,
    'feb': 2,
    'febuary': 2,
    'mar': 3,
    'march': 3,
    'apr': 4,
    'april': 4,
    'may': 5,
    'jun': 6,
    'june': 6,
    'jul': 7,
    'july': 7,
    'aug': 8,
    'august': 8,
    'sep': 9,
    'september': 9,
    'oct': 10,
    'october': 10,
    'nov': 11,
    'november': 11,
    'dec': 12,
    'december': 12
}
