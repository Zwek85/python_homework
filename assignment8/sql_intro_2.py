import sqlite3
import pandas as pd
import os

# Set database path to lesson.db
db_path = "/Users/kaedentun/python_homework/db/lesson.db"

# Connect to the database
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = 1")

# SQL query to join line_items and products
query = """
SELECT
    line_items.line_item_id,
    line_items.quantity,
    products.product_id,
    products.product_name,
    products.price
FROM line_items
JOIN products ON line_items.product_id = products.product_id;
"""

# Load into a DataFrame
df = pd.read_sql_query(query, conn)
print("Raw data (first 5 rows):")
print(df.head())

# Add total column
df['total'] = df['quantity'] * df['price']
print("\nAfter adding 'total' column:")
print(df.head())

# Group by product_id
summary = df.groupby('product_id').agg({
    'line_item_id': 'count',
    'total': 'sum',
    'product_name': 'first'
}).rename(columns={
    'line_item_id': 'order_count',
    'total': 'total_revenue'
})

# Sort by product_name
summary = summary.sort_values('product_name')

# Save to CSV
output_path = os.path.join(os.getcwd(), 'order_summary.csv')
summary.to_csv(output_path, index=False)
print(f"\n✅ Summary written to: {output_path}")

# Close the connection
conn.close()
