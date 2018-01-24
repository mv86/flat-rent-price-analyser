class FlatPriceAverages():
    """Collection of averages for data stored in flat price analysis table for provided month.

       Arguments:
            month: int 1-12 (Jan = 1, Dec = 12)
            calculate_average: function to connect to db and perform select statement

       Instance Variables:
            month: int 1-12 (Jan = 1, Dec = 12)

            monthly_avg: tuple of int averages (mean, median)
            one_bed_avg: tuple of int averages (mean, median)
            two_bed_avg: tuple of int averages (mean, median)
            eh6_avg: tuple of int averages (mean, median)
            eh7_avg: tuple of int averages (mean, median)   
            (None, None) tuple returned for any unavailable average data.
    """
    def __init__(self, month, calculate_average):
        self.month = month
        self.monthly_avg = self._average_of_month(calculate_average)
        self.one_bed_avg = self._average_of('bedrooms', 1, calculate_average)
        self.two_bed_avg = self._average_of('bedrooms', 2, calculate_average)
        self.eh6_avg = self._average_of('postcode_area', 'EH6', calculate_average)
        self.eh7_avg = self._average_of('postcode_area', 'EH7', calculate_average)

    def __repr__(self):
        return f'{self.__class__.__name__}. Month: {self.month}'

    def _average_of_month(self, calculate_average):
        sql = """SELECT price FROM flat_price_analysis 
                 WHERE date_part('month', created_on) = (%s);"""
        monthly_avg = calculate_average(sql, (self.month,))
        return monthly_avg

    def _average_of(self, column, argument, calculate_average):
        sql = f"""SELECT price FROM flat_price_analysis
                  WHERE {column} = (%s)
                  AND date_part('month', created_on) = (%s);"""
        avg = calculate_average(sql, (argument, self.month))
        return avg
