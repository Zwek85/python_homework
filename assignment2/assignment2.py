#task2

import csv
import traceback

def read_employees():
    result = {}
    rows = []
    try:
        with open("../csv/employees.csv", newline='') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    result["fields"] = row
                else:
                    rows.append(row)
        result["rows"] = rows
        return result

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}'
            )
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        exit(1)

# Global variable required for test to work
employees = read_employees()
print(employees)

#task3

def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")

print(f"The index of employee_id column is {employee_id_column}")

#task4
def first_name(row_num):
    col= column_index("first_name")
    return employees["rows"][row_num][col]

#task5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches = list(filter(employee_match, employees["rows"]))
    return matches

#task6
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

#task7
def sort_by_last_name():
    last_name_col = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_col])
    return employees["rows"]
sort_by_last_name()
print(employees)

#task8
def employee_dict(row):
    return {field: value for field, value in zip(employees["fields"], row) if field != "employee_id"}

# test call
print(employee_dict(employees["rows"][0]))

#task9
def all_employees_dict():
    result = {}
    for row in employees["rows"]:
        employee_id = row[column_index("employee_id")]
        result[employee_id] = employee_dict(row)
    return result

#task10
import os

def get_this_value():
    return os.getenv("THISVALUE")
print(get_this_value())

#task11
import custom_module

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("Pasta is good")
print(custom_module.secret)  

#task12
import csv

def read_csv_as_dict(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        fields = next(reader)
        rows = [tuple(row) for row in reader]
        return {"fields": fields, "rows": rows}

def read_minutes():
    minutes1 = read_csv_as_dict("../csv/minutes1.csv")
    minutes2 = read_csv_as_dict("../csv/minutes2.csv")
    return minutes1, minutes2

# Global vars
minutes1, minutes2 = read_minutes()

print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

#task13
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    return set1.union(set2)

minutes_set = create_minutes_set()
print("Combined minutes:", minutes_set)

#task14
from datetime import datetime

def create_minutes_list():
    raw_list = list(minutes_set)
    converted = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), raw_list)
    return list(converted)

minutes_list = create_minutes_list()
print("Minutes List:", minutes_list)

#task15
import csv
from datetime import datetime

def write_sorted_list():
    # sort minutes_list by datetime
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    # Convert datetime back to string using strftime
    converted = list(map(
        lambda x: (x[0], x[1].strftime("%B %d, %Y")),
        sorted_list
    ))

    # Write to ./minutes.csv
    with open("./minutes.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(minutes1["fields"])  # Write header row
        writer.writerows(converted)          # Write each (name, date_string)

    # Return the converted list
    return converted

written_minutes = write_sorted_list()
print("Sorted and written minutes:", written_minutes)















