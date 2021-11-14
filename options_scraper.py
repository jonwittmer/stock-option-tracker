import requests
from datetime import datetime
from bs4 import BeautifulSoup

class OptionInfo():
    def __init__(self, option_type, contract, strike, last, bid, ask, volume, iv):
        self.option_type = option_type
        self.contract = contract
        self.strike = strike
        self.last = last
        self.bid = bid
        self.ask = ask
        self.volume = volume
        self.iv = iv

class StockOptionsScraper():
    def __init__(self) -> None:
        self.maximum_expiry_period_days = 2 * 30 

        # header makes it so it looks like we are a browser and not a scraper
        self.requests_headers = {
                'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language' : 'en-US,en;q=0.5',
                'DNT'             : '1', # Do Not Track Request Header
                'Connection'      : 'close'
            }
        return
    
    def buildUrl(self, stock_symbol: str) -> str:
        base_url = "https://finance.yahoo.com/quote/{}/options"
        return base_url.format(stock_symbol)

    def getOptionsTables(self, stock_symbol: str):
        url = self.buildUrl(stock_symbol)
        data_html = requests.get(url, headers=self.requests_headers).content
        content = BeautifulSoup(data_html, "html.parser")
        options_tables = content.find_all("table")
        calls_tables = self.getTables(options_tables[0], "call")
        puts_tables = self.getTables(options_tables[1], "put")
        return {"calls": calls_tables, "puts": puts_tables}

    def getTables(self, tables, option_type) -> dict:
        calls = tables.find_all("tr")[1:]
        processed_tables = {}
        processed_tables["in-the-money"] = []
        processed_tables["out-of-the-money"] = []
        for option in calls:
            # yahoo finance does not provide the name of the data member as part of the
            # structure holding fields, so for now, the locations of each field are hardcoded
            raw_option_info = BeautifulSoup(str(option), "html.parser").find_all("td")
            info_obj = OptionInfo(option_type, raw_option_info[0].text, raw_option_info[2].text, raw_option_info[3].text,
                                  raw_option_info[4].text, raw_option_info[5].text, raw_option_info[8].text,
                                  raw_option_info[10].text)
            
            if "in-the-money" in str(option):    
                processed_tables["in-the-money"].append(info_obj)
            else:
                processed_tables["out-of-the-money"].append(option)
        return processed_tables

    def prettyPrintTable(self, table):
        for key, val in table.items():
            print("{}:".format(key))
            for option in val:
                for name, prop in vars(option).items():
                    print("{}: {}  ".format(name, prop), end='', flush=False)
                print()
