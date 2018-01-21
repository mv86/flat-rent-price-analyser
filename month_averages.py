"""Contains FlatPriceAverages class for calculating all averages for provided month"""


class FlatPriceAverages():
    """Collection of averages for data stored in flat price analysis table for provided month.
       Arguments:
            month: int 1-12 (Jan = 1, Dec = 12)
            calculate_average: function to connect to and select from db 
    """
    def __init__(self, month, calculate_average):
        self.month = month
        self.calculate_average = calculate_average
        self.monthly_avg = self.average_of_month()
        self.one_bed_avg = self.average_of('bedrooms', 1)
        self.two_bed_avg = self.average_of('bedrooms', 2)
        self.eh6_avg = self.average_of('postcode_area', 'EH6')
        self.eh7_avg = self.average_of('postcode_area', 'EH7')

    def average_of_month(self):
        """TODO"""
        sql = """SELECT price FROM flat_price_analysis 
                 WHERE date_part('month', created_on) = (%s);"""
        monthly_avg = self.calculate_average(sql, (self.month,))
        return monthly_avg

    def average_of(self, column, argument):
        """TODO"""
        sql = f"""SELECT price FROM flat_price_analysis
                  WHERE {column} = (%s)
                  AND date_part('month', created_on) = (%s);"""
        avg = self.calculate_average(sql, (argument, self.month))
        return avg
