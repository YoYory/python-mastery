import readrides
from collections import Counter

rows = readrides.read_rides("Data/ctabus.csv", "dict")

# (d) 1. How many bus routes exist in Chicago?
bus_routes = {row["route"] for row in rows}
print(f"{len(bus_routes)=}")

# (d) 2. How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
def count_people(rows, route, date):
    p_total = 0
    for r in (row for row in rows if (row['date'] == date and row['route'] == route)):
        p_total += r['rides']
    return p_total

print(f"{count_people(rows, "22", "02/02/2011")}")

# (d) 3. What is the total number of rides taken on each bus route?
p_total_per_route = Counter()
for r in rows:
    p_total_per_route[r['route']] += r['rides']
print(f"{p_total_per_route=}")

# (d) 4. What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
r_yearly = Counter()
for r in rows:
    r_yearly[(r['route'], r['date'][-4:])] += r['rides']

r_10increase = Counter()
for route in bus_routes:
    r_10increase[route] = r_yearly[(route, '2011')] - r_yearly[(route, '2001')]
print(f"{r_10increase.most_common(5)=}")



