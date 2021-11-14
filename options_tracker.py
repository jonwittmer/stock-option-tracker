import pandas as pd
import numpy as np
from time import sleep
from options_scraper import StockOptionsScraper
from options_analysis import StockOptionsAnalyzer
from stock import Stock

# for now, this only gets the options for the next available date (probably the end of the week)
# eventually, get more data by changing URL

df = pd.read_csv("stock_list.csv", header=0)

# convert dataframe to list of Stock objects
stocks = [Stock(tick, owned) for tick, owned in zip(df["ticker"], df["quantity_owned"])]

# html parser that we use to return tables with stock info
scraper = StockOptionsScraper()

# load stock data once every 10 minutes
fetch_data_period_minutes = 10
fetch_data_period_seconds = fetch_data_period_minutes * 60
while true:
    # get the latest options tables
    for stock in stocks:
        stock.setOptionsTables(scraper.getOptionsTables(stock.symbol))
    
    # make sure  it is working correctly
    analyzer = StockOptionsAnalyzer(stocks)
    analyzer.identifyOpportunities()
    sleep(fetch_data_period_seconds)
    
