import csv
from collections import namedtuple
from collections.abc import Sequence

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


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of dicts
    """
    records = RideData()  # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            records.append(record)
    return records


def read_rides_as_columns(filename):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


class RideData(Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        return len(self.routes)

    def __getitem__(self, item):
        if isinstance(item, int):
            return {
                "route": self.routes[item],
                "date": self.dates[item],
                "daytype": self.daytypes[item],
                "rides": self.numrides[item],
            }
        elif isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            return [
                {
                    "route": self.routes[i],
                    "date": self.dates[i],
                    "daytype": self.daytypes[i],
                    "rides": self.numrides[i],
                }
                for i in range(start, stop, step)
            ]
            # onderstaande code had ik zelf verzonnen maar bovenstaande is efficienter,
            # duidelijker, en minder kans op errors
            # return [self[i] for i in range(len(self))[item]]

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


if __name__ == "__main__":
    import sys
    import tracemalloc

    tracemalloc.start()
    if len(sys.argv) == 2:
        rows = read_rides("Data/ctabus.csv", sys.argv[1])
    else:
        rows = read_rides_as_dicts("Data/ctabus.csv")
    print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    print(rows[0:10])
