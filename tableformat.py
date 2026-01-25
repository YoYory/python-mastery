from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError

    @abstractmethod
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


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


def print_table(records: list, fields: list[str], formatter: TableFormatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Formatter must be of type Tableformatter")
    formatter.headings(fields)
    for row in records:
        rowdata = [getattr(row, field) for field in fields]
        formatter.row(rowdata)
    print("")


def create_formatter(_type, column_formats=None, upper_headers=False):
    if _type == "text":
        Formatter = TextTableFormatter
    elif _type == "html":
        Formatter = HTMLTableFormatter
    elif _type == "csv":
        Formatter = CSVTableFormatter
    else:
        raise NotImplementedError("Choose text, csv or html")
    if column_formats is not None:

        class Formatter(ColumnFormatMixin, Formatter):
            formats = column_formats

    if upper_headers:

        class Formatter(UpperHeadersMixin, Formatter):
            pass
        
    return Formatter()


if __name__ == "__main__":
    import stock, reader

    portfolio = reader.read_csv_as_instances("Data/portfolio.csv", stock.Stock)
    formatter = create_formatter("csv", column_formats=['"%s"', "%d", "%0.2f"])
    print_table(portfolio, ["name", "shares", "price"], formatter)
    formatter = create_formatter("text", upper_headers=True)
    print_table(portfolio, ["name", "shares", "price"], formatter)
    formatter = create_formatter(
        "text", column_formats=['"%s"', "%d", "%0.2f"], upper_headers=True
    )
    print_table(portfolio, ["name", "shares", "price"], formatter)
