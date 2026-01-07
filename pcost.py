def portfolio_cost(filename: str):
    total = 0.0
    with open(filename, "r") as f:
        for line in f:
            split = line.split(sep=" ")
            try:
                total += int(split[1]) * float(split[2])
            except ValueError as e:
                print(f"Couldn't parse: {line.strip()}")
                print(f"Reason: {e}")

    return total

if __name__ == "__main__":
    print(portfolio_cost("Data/portfolio3.dat"))
