import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s OR phone = %s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()

def import_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()

def menu():
    create_table()

    while True:
        print("\n1. Add contact")
        print("2. Show contacts")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Import from CSV")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            add_contact(name, phone)

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            name = input("Name: ")
            new_phone = input("New phone: ")
            update_contact(name, new_phone)

        elif choice == "4":
            value = input("Enter name or phone: ")
            delete_contact(value)

        elif choice == "5":
            filename = input("CSV filename: ")
            import_from_csv(filename)

        elif choice == "6":
            break

        else:
            print("Invalid choice")

menu()
