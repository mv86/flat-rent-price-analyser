## Leith, Edinburgh Flat Rental Price Analyser
#### Python Version: 3.6.4

Prototype to perform weekly web scraping of flat rental infomation.

Criteria: 1 or 2 bedroom flats in Leith, Edinburgh.

Outcome: Analyse the monthly average prices of Leith flats.

### Web Scraping

Anacron job set to run main.py script every 7 days.

Main.py calls the sites package to scrape flat listing websites and store extracted infomation into db.

### Flat Price Analysis

Running display_averages.py script with desired month prints a table with the following information to the terminal:

Count, mean and median average for month totals, one bedroom, two bedrooms, EH6 postcode and EH7 postcode.
