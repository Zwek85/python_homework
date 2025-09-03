#Task2
import sqlite3
import os

def connect_and_create_tables():
    conn = None
    try:
        db_path = '../db/magazines.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON;")

        # To create publishers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        ''')

        # To create magazines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            );
        ''')

        # To create subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            );
        ''')

        # To create subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            );
        ''')

        conn.commit()
        print("All tables created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    connect_and_create_tables()

#Task3
import sqlite3
import os

def connect_to_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'db', 'magazines.db'))

    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = 1")  # Enforce foreign keys
        print("Database connection successful.")
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred connecting to database: {e}")
        return None

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE(name, address)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                PRIMARY KEY (subscriber_id, magazine_id),
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            );
        """)
        conn.commit()
        print("Tables created or verified.")
    except sqlite3.Error as e:
        print(f"An error occurred creating tables: {e}")

# Insert functions with duplicate checking:

def add_publisher(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Publisher '{name}' already exists.")
            return
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Publisher '{name}' added.")
    except sqlite3.Error as e:
        print(f"Error adding publisher '{name}': {e}")

def add_magazine(conn, name, publisher_name):
    try:
        cursor = conn.cursor()
        # Get publisher id
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
        result = cursor.fetchone()
        if not result:
            print(f"Publisher '{publisher_name}' does not exist. Cannot add magazine '{name}'.")
            return
        publisher_id = result[0]

        # Check if magazine exists
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Magazine '{name}' already exists.")
            return

        cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        conn.commit()
        print(f"Magazine '{name}' added.")
    except sqlite3.Error as e:
        print(f"Error adding magazine '{name}': {e}")

def add_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        # Check for duplicate name + address
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
        if cursor.fetchone():
            print(f"Subscriber '{name}' at '{address}' already exists.")
            return
        cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
        print(f"Subscriber '{name}' at '{address}' added.")
    except sqlite3.Error as e:
        print(f"Error adding subscriber '{name}': {e}")

def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        cursor = conn.cursor()
        # Get subscriber id
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, subscriber_address))
        sub_result = cursor.fetchone()
        if not sub_result:
            print(f"Subscriber '{subscriber_name}' at '{subscriber_address}' not found. Cannot add subscription.")
            return
        subscriber_id = sub_result[0]

        # Get magazine id
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
        mag_result = cursor.fetchone()
        if not mag_result:
            print(f"Magazine '{magazine_name}' not found. Cannot add subscription.")
            return
        magazine_id = mag_result[0]

        # Checking if subscription exists
        cursor.execute("""
            SELECT * FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?
        """, (subscriber_id, magazine_id))
        if cursor.fetchone():
            print(f"Subscription for '{subscriber_name}' to '{magazine_name}' already exists.")
            return

        cursor.execute("""
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
        """, (subscriber_id, magazine_id, expiration_date))
        conn.commit()
        print(f"Subscription of '{subscriber_name}' to '{magazine_name}' added.")
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")

def main():
    conn = connect_to_db()
    if not conn:
        return

    create_tables(conn)

    # To add Publishers
    add_publisher(conn, "Technology Publishing")
    add_publisher(conn, "National Geographic")
    add_publisher(conn, "Urban Housing")

    # To add Magazines
    add_magazine(conn, "Python Weekly", "Technology Publishing")
    add_magazine(conn, "Wildlife Today", "National Geographic")
    add_magazine(conn, "Life in the city", "Urban Housing")

    # To add Subscribers
    add_subscriber(conn, "Ally John", "123 Maple St")
    add_subscriber(conn, "Bori Nice", "456 Oak Ave")
    add_subscriber(conn, "Ally John", "789 Pine Rd")  # Same name, different address

    # Add Subscriptions
    add_subscription(conn, "Ally John", "123 Maple St", "Python Weekly", "2025-12-31")
    add_subscription(conn, "Bori Nice", "456 Oak Ave", "Wildlife Today", "2024-06-30")
    add_subscription(conn, "Ally John", "789 Pine Rd", "Life in the city", "2023-11-15")

    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()

#Task4
def run_queries(conn):
    cursor = conn.cursor()

    print("\nAll subscribers:")
    cursor.execute("SELECT * FROM subscribers;")
    subscribers = cursor.fetchall()
    for row in subscribers:
        print(row)

    print("\nAll magazines sorted by name:")
    cursor.execute("SELECT * FROM magazines ORDER BY name;")
    magazines = cursor.fetchall()
    for row in magazines:
        print(row)

    # Find magazines for a particular publisher, e.g. 'TechBooks Publishing'
    publisher_name = "TechBooks Publishing"
    print(f"\nMagazines published by '{publisher_name}':")
    cursor.execute("""
        SELECT magazines.*
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?;
    """, (publisher_name,))
    mags_for_publisher = cursor.fetchall()
    for row in mags_for_publisher:
        print(row)

