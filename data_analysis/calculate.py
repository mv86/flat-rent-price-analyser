"""Calculate monthly average/s of the flat prices stored in flat_price_analysis table"""
import statistics
import db.connect
from .flat_price_averages import FlatPriceAverages


def flat_price_averages_for(month):
    '''Return FlatPriceAverages class containing all averages for passed month'''
    month_averages = FlatPriceAverages(month, _calculate_average)
    return month_averages


def _calculate_average(sql, data):
    flat_prices = db.connect.select(sql, data)
    if flat_prices:
        # Unpack list of tuples into a list of ints
        flat_prices = [price[0] for price in flat_prices]
        median_price = statistics.median(flat_prices)
        mean_price = statistics.mean(flat_prices)
        return int(mean_price), int(median_price)
    return None, None
