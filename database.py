import sqlite3

conn = sqlite3.connect('customer.db') #create a database

#create a cursor
c = conn.cursor()

#create a table
# c.execute("""CREATE TABLE students (
#     first_name text,
#     last_name text,
#     email text
# )
# """)
# customers= [('Stefan', 'Salcianu', 'stefan.salcianu26@gmail.com'), 
#             ('Mateu', 'ciprian', 'matei@codemy.com'), 
#             ('Elthon', 'John', 'john@codemy.com'),
#             ('Henry', 'Elder', 'henry@codemy.com')]
# c.executemany("""INSERT INTO customers VALUES (?, ?, ?)""", customers)
c.execute("SELECT rowid, * FROM customers WHERE rowid BETWEEN 1 AND 10")
def afisareFancy():
    items=c.fetchall()
    for item in items:
        print(item)
afisareFancy()
c.execute("UPDATE customers SET first_name='Stefan' WHERE rowid%2=0")
conn.commit() 
print("AFTER UPDATE:-------")
c.execute("SELECT rowid, * FROM customers WHERE rowid BETWEEN 1 AND 10")
afisareFancy()
# c.execute("DELETE FROM customers")
# conn.commit() 
print("AFTER UPDATE:-------")
c.execute("SELECT rowid, last_name FROM customers WHERE rowid BETWEEN 1 AND 10 order by last_name desc Limit 2")
afisareFancy()
# c.execute("Drop table customers") Deletes a table
# conn.commit() 
conn.close()