#!/home/max/Python/projects/flat_price_analyser/venv/bin/python
"""Print table of average flat prices to terminal for passed month parameter.
    
   Arguments:
        Month: Full month name or 3 letter abreviation, eg. Jan/January
"""
import sys
from tabulate import tabulate
from data_analysis import calculate


def _display_averages_for(month):
    month = _validate_month(month)
    
    # Unpack flat price averages
    month_averages = calculate.flat_price_averages_for(month)
    total_mean, total_median = month_averages.monthly_avg
    one_bed_mean, one_bed_median = month_averages.one_bed_avg
    two_bed_mean, two_bed_median = month_averages.two_bed_avg
    eh6_mean, eh6_median = month_averages.eh6_avg
    eh7_mean, eh7_median = month_averages.eh7_avg

    # Create table to print to terminal
    headers = ['Type', 'Mean', 'Median']
    table = [
        ['Total', total_mean, total_median],
        ['One Bed', one_bed_mean, one_bed_median],
        ['Two Bed', two_bed_mean, two_bed_median],
        ['EH6', eh6_mean, eh6_median],
        ['EH7', eh7_mean, eh7_median]
    ]
    print(tabulate(table, headers, tablefmt='psql')) 


def _validate_month(month):
    if not isinstance(month, str):
        raise TypeError('String is required for month argument')
    # If month is valid return as int representation understood by Postgresql
    month = month.lower().strip()
    if month in MONTH_DICTIONARY:
        sql_month = MONTH_DICTIONARY[month]
        return sql_month
    else:
        raise ValueError(
            "Valid format for month: full name or three letter abreviation"
        )

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

def main():
    """Entry point to script"""
    if len(sys.argv) == 2:
        month = sys.argv[1]
        _display_averages_for(month)
    else:
        raise ValueError('1 argument expected: str month, e.g Jan or January')

if __name__ == '__main__':
    main()
