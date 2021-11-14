

class Stock():
    def __init__(self, symbol, quantity_owned):
        self.symbol = symbol
        self.price = 0
        self.quantity_owned = quantity_owned
        self.options_tables = None

    def getOwnedValue(self) -> float:
        return self.price * self.quantity_owned

    def identifyOpportunities(self):
        pass

    # needed so we can use list comprehension to call this
    def setOptionsTables(self, tables):
        self.options_tables = tables
        
