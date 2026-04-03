import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="morjinka",
        password="",
        host="localhost",
        port="5432"
    )
def lab8_1func(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "select * from find(%s);",
        (pattern,)
    )
    rows = cur.fetchall()

    for name, phone in rows:
        print (f"{name}: {phone}")
    cur.close()
    conn.close()

def lab8_func2(new_name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "call add_contact(%s, %s);",
        (new_name, new_phone)
        )

    conn.commit()
    cur.close()
    conn.close()

def lab8_func3(names, phones):
    conn = connect()
    cur = conn.cursor()

    cur.execute( 
                "CALL insert_many_contacts(%s::text[], %s::text[]);",
                (names, phones)
            )

    cur.execute("SELECT * FROM invalid_contacts;")
    rows = cur.fetchall()

    if rows:
        print("Invalid:")
        for row in rows:
            print(row)
    conn.commit()
    cur.close()
    conn.close()

def lab8_func4(num1, num2):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
    "select * from paginated_contacts(%s, %s);",
    (num1, num2)
    )

    rows = cur.fetchall()
    for Id, name, phone in rows:
        print(f"{id} - {name}: {phone}")
    
    conn.commit()
    cur.close()
    conn.close()
    
def lab8_func5(username, phone):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(
        "call delete_data(%s, %s);",
        (phone, username)
        )
    conn.commit()
    cur.close()
    conn.close()

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
        print("lab8")
        print("7. find by pattetn")
        print("8. insert or update")
        print("9. insert many user")
        print("10. queries data")
        print("11. delete")

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

        elif choice == "7":
            pattern = input("Pattern: ")
            lab8_1func(pattern)

        elif choice == "8":
            name = input("Name: ")
            phone = input("Phone: ")
            lab8_func2(name, phone)

        elif choice == "9":
            names = input("Names: ").split()
            phones = input("Phones: ").split()
            if len(names) != len(phones):
                print("Names and phones counts must match")
            else:
                lab8_func3(names, phones)

        elif choice == "10":
            limit = int(input("how many contacts: "))
            offset = int(input("Offset: "))
            lab8_func4(limit + 1, offset)

        elif choice == "11":
            name = input("Name: ")
            phone = input("Phone: ")
            lab8_func5(name, phone)

        else:
            print("Invalid choice")

menu()
