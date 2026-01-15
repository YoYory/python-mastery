import stock


def print_table(objects: list, attributes: list[str]):
    for att in attributes:
        print(f"{att:>10s}", end=" ")
    print("\n" + ("-" * 10 + " ") * len(attributes))
    for obj in objects:
        for att in attributes:
            print(f"{str(getattr(obj, att)):>10s}", end=" ")
        print('')
    print('')


port = stock.read_portfolio("Data/portfolio.csv")
print_table(port, ["name", "shares", "price"])
print_table(port, ["shares", "name"])
