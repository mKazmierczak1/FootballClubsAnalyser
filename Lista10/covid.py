from datetime import datetime, timedelta
from types import NoneType

all_cases = []
by_date = {}
by_country = {}
by_continent = {}
file_path = '.\\Covid.txt'

def load_data_from_file():
    file = open(file_path, 'r', encoding="utf-8")

    file_content =  file.read()
    records = file_content.split('\n')

    for i in range(1, len(records)):
        cases = records[i].split("\t")
        case = (cases[6], cases[3], cases[2], cases[1], cases[5], cases[4], cases[10])
        
        all_cases.append(case)
        by_date[(case[1], case[2], case[3])] = []
        by_country[case[0]] = []
        by_continent[case[6]] = []

    for case in all_cases:
        by_date.get((case[1], case[2], case[3])).append((case[0], case[4], case[5]))
        by_country.get(case[0]).append((case[1], case[2], case[3], case[4], case[5]))

        if not case[0] in by_continent.get(case[6]):
            by_continent.get(case[6]).append(case[0])

load_data_from_file()

def get_countries():
    return by_country.keys()

def get_continents():
    return by_continent.keys()

def is_continent(territory):
    return territory in by_continent.keys()

def check_territory(country, territory):
    if is_continent(territory):
        return country in by_continent[territory]
    else:
        return country == territory 

def show_total(date: datetime, territory, type_of_data):
    d = 2 if type_of_data == "cases" else 1
    total = 0
    value = by_date.get((str(date.year), str(date.month), str(date.day)))
    
    if not isinstance(value, NoneType):
        for v in value:
            if check_territory(v[0], territory):
                total += int(v[d])
    else:
        return "Wrong arguments for " + str(date.date()) + " and " + territory +  "!"
    
    if total == 0:
        return "No data found for " + str(date.date()) + " and " + territory +  "!"
    else:
        return total

def show_total_from_period(start_date: datetime, end_date: datetime, territory, type_of_data):
    days = (end_date - start_date).days

    if days < 0:
        return "Wrong dates!"

    x = start_date
    total = 0

    for i in range (0, days + 1):
        t = show_total(x, territory, type_of_data)
        total += 0 if isinstance(t, str) else t
        x += timedelta(days=1)
    
    return total

def show_total_from_month(month, territory, type_of_data):
    x = datetime(2020, month, 1)
    total = 0

    while x.month == month:
        t = show_total(x, territory, type_of_data)
        total += 0 if t == isinstance(t, str) else t
        x += timedelta(days=1)
    
    return total

def show_records(date: datetime, territory, type_of_data):
    d = 2 if type_of_data == "cases" else 1
    value = by_date.get((str(date.year), str(date.month), str(date.day)))
    records = []

    if not isinstance(value, NoneType):
        for v in value:
            if check_territory(v[0], territory):
                records.append((date.date(), v[0], int(v[d])))
    else:
        return "Wrong arguments for " + str(date.date()) + " and " + territory +  "!"
    
    return records

def show_records_from_period(start_date: datetime, end_date: datetime, territory, type_of_data):
    days = (end_date - start_date).days

    if days < 0:
        return "Wrong dates!"

    x = start_date
    records = []

    for i in range (0, days + 1):
        records += show_records(x, territory, type_of_data)
        x += timedelta(days=1)
    
    return records

def show_records_from_month(month, territory, type_of_data):
    x = datetime(2020, month, 1)
    records = []

    while x.month == month:
        records += show_records(x, territory, type_of_data)
        x += timedelta(days=1)
    
    return records

def set_file_path(path):
    global file_path
    file_path = path
    all_cases.clear()
    by_country.clear()
    by_date.clear()
    by_continent.clear()
    load_data_from_file()