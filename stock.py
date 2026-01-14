import csv


class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


def read_portfolio(filename: str):
    stocks = []
    types = [str, int, float]
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            row = [func(val) for func, val in zip(types, row)]
            stocks.append(Stock(*row))
    return stocks


def print_portfolio(port: list[Stock]):
    print("%10s %10s %10s" % ("name", "shares", "price"))
    print(("-" * 10 + " ") * 3)
    for s in port:
        print("%10s %10d %10.2f" % (s.name, s.shares, s.price))


portfolio = read_portfolio("Data/portfolio.csv")
print_portfolio(portfolio)
