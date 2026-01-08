import csv
from collections import namedtuple

Row = namedtuple("Row", ["route", "date", "daytype", "rides"])


class Rowclass:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class Rowclass_slots:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def create_record(route, date, daytype, rides, record_type):
    if record_type == "tuple":
        return (route, date, daytype, rides)
    if record_type == "dict":
        return {
            "route": route,
            "date": date,
            "daytype": daytype,
            "rides": rides,
        }
    if record_type == "class":
        return Rowclass(route, date, daytype, rides)
    if record_type == "namedtuple":
        return Row(route, date, daytype, rides)
    if record_type == "class_slots":
        return Rowclass_slots(route, date, daytype, rides)


def read_rides(filename, record_type="tuple"):
    """
    Read the bus ride data as a list of records
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = create_record(route, date, daytype, rides, record_type)
            records.append(record)
    return records


if __name__ == "__main__":
    import sys
    import tracemalloc

    tracemalloc.start()
    if len(sys.argv) == 2:
        rows = read_rides("Data/ctabus.csv", sys.argv[1])
    else:
        rows = read_rides("Data/ctabus.csv", "tuple")
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
