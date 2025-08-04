#list-comprehensions

import csv

# Read the CSV into a list of rows
with open("../csv/employees.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Skip the header 
data_rows = rows[1:]

# List comprehension to create full names
full_names = [f"{row[0]} {row[1]}" for row in data_rows]
print("All Employee Names:")
print(full_names)

# List comprehension to filter names with the letter 'e' 
names_with_e = [name for name in full_names if 'e' in name.lower()]
print("\nNames containing the letter 'e':")
print(names_with_e)
