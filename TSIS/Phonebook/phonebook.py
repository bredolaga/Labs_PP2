import csv
import json
from connect import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    with open("schema.sql", "r") as file:
        cur.execute(file.read())

    with open("procedures.sql", "r") as file:
        cur.execute(file.read())

    with open("functions.sql", "r") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
    """, (name, email, birthday, group_id))

    conn.commit()
    cur.close()
    conn.close()


def add_phone_to_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Type home/work/mobile: ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()


def move_contact_to_group():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Contact name: ")
    group_name = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.name
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_contacts():
    conn = get_connection()
    cur = conn.cursor()

    q = input("Search: ")

    cur.execute("SELECT * FROM unified_search(%s)", (q,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()

    group_name = input("Group: ")

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
        ORDER BY c.name
    """, (group_name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    conn = get_connection()
    cur = conn.cursor()

    email = input("Email pattern: ")

    cur.execute("""
        SELECT name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name
    """, ("%" + email + "%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()

    print("1 name")
    print("2 birthday")
    print("3 date_added")

    choice = input("> ")

    if choice == "1":
        order_column = "name"
    elif choice == "2":
        order_column = "birthday"
    else:
        order_column = "date_added"

    cur.execute(f"""
        SELECT name, email, birthday, date_added
        FROM contacts
        ORDER BY {order_column}
    """)

    rows = cur.fetchall()

    for name, email, birthday, date_added in rows:
        print(f"{name} | {email} | {birthday} | {date_added}")

    cur.close()
    conn.close()


def paginate_contacts():
    conn = get_connection()
    cur = conn.cursor()

    limit = 5
    offset = 0

    while True:
        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cmd = input("next/prev/quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

    cur.close()
    conn.close()


def import_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    filename = input("CSV filename: ")

    with open(filename, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            name = row[0]
            phone = row[1]

            email = ""
            birthday = None
            group_name = "Other"
            phone_type = "mobile"

            if len(row) > 2:
                email = row[2]
            if len(row) > 3 and row[3] != "":
                birthday = row[3]
            if len(row) > 4 and row[4] != "":
                group_name = row[4]
            if len(row) > 5 and row[5] != "":
                phone_type = row[5]

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group_name,))

            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
            """, (name, email, birthday, group_id))

            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()


def export_to_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)

    contacts = cur.fetchall()
    result = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
        """, (contact_id,))

        phones = cur.fetchall()

        result.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "group": contact[4],
            "phones": [
                {"phone": p[0], "type": p[1]}
                for p in phones
            ]
        })

    with open("contacts.json", "w") as file:
        json.dump(result, file, indent=4)

    cur.close()
    conn.close()

    print("Exported to contacts.json")


def import_from_json():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json", "r") as file:
        data = json.load(file)

    for contact in data:
        name = contact["name"]
        email = contact["email"]
        birthday = contact["birthday"]
        group_name = contact["group"]

        cur.execute("""
            INSERT INTO groups(name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (group_name,))

        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        group_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
        """, (name, email, birthday, group_id))

        for phone in contact["phones"]:
            cur.execute("CALL add_phone(%s, %s, %s)", (
                name,
                phone["phone"],
                phone["type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from contacts.json")


def menu():
    create_tables()

    while True:
        print("1 Add contact")
        print("2 Add phone")
        print("3 Move to group")
        print("4 Show contacts")
        print("5 Search")
        print("6 Filter by group")
        print("7 Search by email")
        print("8 Sort contacts")
        print("9 Pagination")
        print("10 Import from CSV")
        print("11 Export to JSON")
        print("12 Import from JSON")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone_to_contact()
        elif choice == "3":
            move_contact_to_group()
        elif choice == "4":
            show_contacts()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            paginate_contacts()
        elif choice == "10":
            import_from_csv()
        elif choice == "11":
            export_to_json()
        elif choice == "12":
            import_from_json()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


menu()
