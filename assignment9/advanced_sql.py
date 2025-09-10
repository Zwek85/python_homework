import sqlite3
#task1
def main():
    # Connect to the database (adjust path if needed)
    conn = sqlite3.connect('../db/lesson.db')
    cursor = conn.cursor()

    # Task 1: Aggregation query with join on products and line_items
    sql = '''
    SELECT
        line_items.product_id,
        products.product_name,
        SUM(line_items.quantity) AS total_quantity,
        SUM(products.price * line_items.quantity) AS total_sales
    FROM
        line_items
    JOIN
        products ON line_items.product_id = products.product_id
    GROUP BY
        line_items.product_id, products.product_name
    ORDER BY
        total_sales DESC
    LIMIT 5;
    '''

    cursor.execute(sql)
    rows = cursor.fetchall()

    # Print header
    print(f"{'Product ID':<12} {'Product Name':<30} {'Total Quantity':<15} {'Total Sales':<12}")
    print("-" * 75)

    # Print each row
    for product_id, product_name, total_quantity, total_sales in rows:
        print(f"{product_id:<12} {product_name:<30} {total_quantity:<15} ${total_sales:.2f}")

    # Clean up
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

#task2

def print_average_order_price_per_customer(cursor):
    query = """
    SELECT
        c.customer_name,
        AVG(sub.total_price) AS average_total_price
    FROM
        customer c
    LEFT JOIN
        (
            SELECT
                o.customer_id AS customer_id_b,
                SUM(oi.quantity * oi.unit_price) AS total_price
            FROM
                orders o
            JOIN
                order_items oi ON o.order_id = oi.order_id
            GROUP BY
                o.order_id, o.customer_id
        ) sub
    ON
        c.customer_id = sub.customer_id_b
    GROUP BY
        c.customer_id, c.customer_name;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    
    for row in results:
        customer_name, average_total_price = row
        print(f"Customer: {customer_name}, Average Order Price: {average_total_price}")

#Task3 
import sqlite3

def create_order_for_perez():
    conn = sqlite3.connect('../db/lesson.db')  # db path
    conn.execute("PRAGMA foreign_keys = 1")    # Enabling FK constraints
    cursor = conn.cursor()

    try:
        # Begin transaction
        conn.execute("BEGIN")

        # Get customer_id
        cursor.execute("SELECT customer_id FROM customer WHERE customer_name = ?", ("Perez and Sons",))
        customer_id = cursor.fetchone()[0]

        # Get employee_id
        cursor.execute("SELECT employee_id FROM employee WHERE employee_name = ?", ("Miranda Harris",))
        employee_id = cursor.fetchone()[0]

        # Get 5 least expensive product_ids
        cursor.execute("SELECT product_id FROM product ORDER BY unit_price ASC LIMIT 5")
        product_ids = [row[0] for row in cursor.fetchall()]

        # Insert order and get order_id
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, order_date)
            VALUES (?, ?, DATE('now'))
            RETURNING order_id
        """, (customer_id, employee_id))
        order_id = cursor.fetchone()[0]

        # Insert line_items: 10 of each product
        for pid in product_ids:
            cursor.execute("""
                INSERT INTO line_item (order_id, product_id, quantity)
                VALUES (?, ?, ?)
            """, (order_id, pid, 10))

        # Commit 
        conn.commit()

        # Print inserted line items
        cursor.execute("""
            SELECT
                li.line_item_id,
                li.quantity,
                p.product_name
            FROM
                line_item li
            JOIN
                product p ON li.product_id = p.product_id
            WHERE
                li.order_id = ?
        """, (order_id,))

        results = cursor.fetchall()
        print(f"\n✅ Order ID {order_id} created successfully!\nLine Items:")
        for line_item_id, quantity, product_name in results:
            print(f"- Line Item ID: {line_item_id}, Product: {product_name}, Quantity: {quantity}")

    except Exception as e:
        conn.rollback()
        print("❌ Transaction failed:", e)
    finally:
        conn.close()

#Task 4
import sqlite3

def employees_with_more_than_5_orders():
    conn = sqlite3.connect('../db/lesson.db')  #db path
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                e.employee_id,
                e.employee_name,
                COUNT(o.order_id) AS order_count
            FROM
                employee e
            JOIN
                orders o ON e.employee_id = o.employee_id
            GROUP BY
                e.employee_id
            HAVING
                COUNT(o.order_id) > 5;
        """)
        
        results = cursor.fetchall()
        print("\n✅ Employees with more than 5 orders:\n")
        for employee_id, employee_name, order_count in results:
            print(f"- ID: {employee_id}, Name: {employee_name}, Orders: {order_count}")

    except Exception as e:
        print("❌ Failed to fetch employees:", e)
    finally:
        conn.close()



