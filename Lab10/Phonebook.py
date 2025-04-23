import psycopg2
import csv

# connect to postgres tables
def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# insert from csv
def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                try:
                    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
                except Exception as e:
                    print(f"Error inserting {row}: {e}")
    conn.commit()
    cur.close()
    conn.close()

# insert from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("Entry added.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# update data
def update_data():
    field = input("Update (1) Name or (2) Phone? Enter 1 or 2: ")
    identifier = input("Search by phone or name: ")
    new_value = input("Enter new value: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        if field == "1":
            cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s OR first_name = %s", (new_value, identifier, identifier))
        elif field == "2":
            cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s OR first_name = %s", (new_value, identifier, identifier))
        conn.commit()
        print("Update successful.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# query data (filter search)
def query_data():
    field = input("Filter by (1) Name or (2) Phone? Enter 1 or 2: ")
    value = input("Enter filter value: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        if field == "1":
            cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{value}%",))
        elif field == "2":
            cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{value}%",))
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# delete data
def delete_data():
    value = input("Enter name or phone to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone = %s", (value, value))
        conn.commit()
        print("Deleted.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

# menu
if __name__ == '__main__':
    create_table()
    print("PhoneBook Ready.")
    while True:
        print("""
Choose an action:
1. Insert from CSV file
2. Insert from console
3. Update entry
4. Query entries
5. Delete entry
6. Exit
        """)
        choice = input("Enter choice (1-6): ")
        if choice == "1":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")