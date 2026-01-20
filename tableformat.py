class TableFormatter:
    def headings(self, headers):
        raise NotImplementedError

    def row(self, rowdata):
        raise NotImplementedError


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(map(str, rowdata)))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr> " + " ".join(f"<th>{header}</th>" for header in headers) + " </tr>")

    def row(sefl, rowdata):
        print("<tr> " + " ".join(f"<td>{item}</td>" for item in rowdata) + " </tr>")

def print_table(records: list, fields: list[str], formatter: TableFormatter):
    formatter.headings(fields)
    for row in records:
        rowdata = [getattr(row, field) for field in fields]
        formatter.row(rowdata)
    print("")

def create_formatter(_type):
    if _type == 'text':
        return TextTableFormatter()
    if _type == 'html':
        return HTMLTableFormatter()
    if _type == 'csv':
        return CSVTableFormatter()
    raise NotImplementedError("Choose text, csv or html")


if __name__ == "__main__":
    import stock, reader
    portfolio = reader.read_csv_as_instances("Data/portfolio.csv", stock.Stock)
    formatter = create_formatter('html')
    print_table(portfolio, ["name", "shares", "price"], formatter)
