import sqlite3
import os

# Absolute path to lesson.db
db_path = "/Users/kaedentun/python_homework/db/lesson.db"

# Ensure the db folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = 1")

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS line_items;")
cursor.execute("DROP TABLE IF EXISTS products;")

# Create the products table
cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
);
""")

# Create the line_items table
cursor.execute("""
CREATE TABLE line_items (
    line_item_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# Insert data into products
products = [
    (1, 'Notebook', 3.5),
    (2, 'Pen', 1.25),
    (3, 'Backpack', 25.0)
]
cursor.executemany("INSERT INTO products VALUES (?, ?, ?);", products)

# Insert data into line_items
line_items = [
    (1, 1, 2),
    (2, 2, 5),
    (3, 3, 1),
    (4, 1, 1)
]
cursor.executemany("INSERT INTO line_items VALUES (?, ?, ?);", line_items)

# Commit and close
conn.commit()
conn.close()

print("✅ lesson.db has been set up with sample data.")
