import sqlite3

conn = sqlite3.connect('customer.db')

c = conn.cursor()

def show_all():
    c.execute("SELECT rowid, * FROM customers")
    items = c.fetchall()
    for item in items:
        print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]}")
    print("Command executed successfully..........................")
def add_one(first, last, email):
    c.execute("INSERT INTO customers "
    "VALUES (?, ?, ?)", (first, last, email))
    conn.commit()
def delete_one(id):
    c.execute("DELETE from customers WHERE rowid = (?)", id)
    conn.commit()
def add_many(List):
    c.executemany("INSERT INTO customers VALUES (?, ?, ?)", (List))
    conn.commit()
