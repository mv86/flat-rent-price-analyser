"""Calculate monthly average/s of the flat prices stored in flat_price_analysis table"""
import statistics
import db.connect


def flat_price_averages_for(month):
    '''Return list of tuples containing all averages for passed month.
       
       Tuple = (query type, type count, mean avg, median avg).
    '''
    month_averages = [
        ('Month Total', *_average_of_month(month)),
        ('One Bedroom', *_average_of('bedrooms', 1, month)),
        ('Two Bedroom', *_average_of('bedrooms', 2, month)),
        ('EH6 Postcode', *_average_of('postcode_area', 'EH6', month)),
        ('EH7 Postcode', *_average_of('postcode_area', 'EH7', month)) 
    ]
    return month_averages


def _average_of_month(month):
    sql = """SELECT price FROM flat_price_analysis 
             WHERE date_part('month', created_on) = (%s);"""
    monthly_avg = _calculate_average(sql, (month,))
    return monthly_avg


def _average_of(column, argument, month):
    sql = f"""SELECT price FROM flat_price_analysis
              WHERE {column} = (%s)
              AND date_part('month', created_on) = (%s);"""
    avg = _calculate_average(sql, (argument, month))
    return avg


def _calculate_average(sql, data):
    flat_prices = db.connect.select(sql, data)
    if flat_prices:
        # Unpack list of tuples into a list of ints
        flat_prices = [price[0] for price in flat_prices]
        count = len(flat_prices)
        mean_price = statistics.mean(flat_prices)
        median_price = statistics.median(flat_prices)
        return count, int(mean_price), int(median_price)
    return 0, None, None
