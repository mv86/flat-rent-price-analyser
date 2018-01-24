"""Calculate monthly average/s of the flat prices stored in flat_price_analysis table"""
import statistics
import db.connect
from flat_price_averages import FlatPriceAverages


def calculate_average_for(month):
    '''Return FlatPriceAverages class containing all averages for passed month'''
    month = validate_month(month)
    month_averages = FlatPriceAverages(month, calculate_average)
    return month_averages


def validate_month(month):
    """Check for TypeError and ValueError in data. Return month as int if data valid."""
    if not isinstance(month, str):
        raise TypeError('String is required for month argument')

    month = month.lower().strip()
    if month in MONTH_DICTIONARY:
        sql_month = MONTH_DICTIONARY[month]
        return sql_month
    else:
        raise ValueError(
            "Valid format for month: full name or three letter abreviation"
        )


def calculate_average(sql, data):
    """Connect to db and calculate flat price mean and median averages for passed data.
       Return tuple (int(mean), int(median)), or (None, None) if no data found.
    """
    flat_prices = db.connect.select(sql, data)
    if flat_prices:
        # Unpack list of tuples into a list of ints
        flat_prices = [price[0] for price in flat_prices]
        median_price = statistics.median(flat_prices)
        mean_price = statistics.mean(flat_prices)
        return int(mean_price), int(median_price)
    return None, None


MONTH_DICTIONARY = {
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

