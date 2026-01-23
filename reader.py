import csv
from collections.abc import Sequence
from abc import ABC, abstractmethod


class DataCollection(Sequence):
    def __init__(self, headings):
        self.data = {k: [] for k in headings}

    def __len__(self):
        return len(self.data[list(self.data.keys())[0]])

    def __getitem__(self, item):
        if isinstance(item, int):
            data = [self.data[column][item] for column in self.data]
            return dict(zip(self.data.keys(), data))
        elif isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            return [
                dict(
                    zip(
                        self.data.keys(), [self.data[column][i] for column in self.data]
                    )
                )
                for i in range(start, stop, step)
            ]

    def append(self, d):
        for key in d:
            self.data[key].append(d[key])


def read_csv_as_columns(filename: str, types: list):
    """
    Read a csv into lists, representing columns
    """
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        records = DataCollection(headings)
        for row in rows:
            record = {name: func(val) for name, func, val in zip(headings, types, row)}
            records.append(record)
    return records


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return {name: func(val) for name, func, val in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_dicts(filename: str, types: list[str]):
    parser = DictCSVParser(types)
    return parser.parse(filename)


def read_csv_as_instances(filename: str, cls: type):
    """
    Read a CSV file into a list of instances
    """
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    from sys import intern

    rows = read_csv_as_columns("Data/ctabus.csv", [intern, intern, intern, int])
    print(len(rows))
    print(rows[0])
    print(rows[10])
    print(rows[0:2])
    print(tracemalloc.get_traced_memory())
