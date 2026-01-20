class Stock:
    _types = (str, int, float)

    __slots__ = ('name', '_price', '_shares')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def shares(self):
        return self._shares
    
    @shares.setter
    def shares(self, value):
        if isinstance(value, self._types[1]) and value >= 0:
            self._shares = value
        else:
            raise TypeError(f"Must be a positive {self._types[1].__name__}")
        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if isinstance(value, self._types[2]) and value >= 0.0:
            self._price = value
        else:
            raise TypeError(f"Must be a positive {self._types[2].__name__}")

    @classmethod
    def from_row(cls, row):
        return cls(*[func(val) for func, val in zip(cls._types, row)])

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


def print_portfolio(port: list[Stock]):
    print("%10s %10s %10s" % ("name", "shares", "price"))
    print(("-" * 10 + " ") * 3)
    for s in port:
        print("%10s %10d %10.2f" % (s.name, s.shares, s.price))

s = Stock('GOOG', 100, 490.1)
