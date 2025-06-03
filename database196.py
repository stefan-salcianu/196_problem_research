import sqlite3
import time

fout = open("history.txt","a")
def delete_table(table_name):
    conn = sqlite3.connect("history.db")
    c= conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
def create_table(name):
    conn = sqlite3.connect("history.db")
    c= conn.cursor()
    c.execute(f""" CREATE TABLE {name} (
            numbers text,
            result boolean,
            iterations integer,
            palindrome text,
            length integer,
            date timestamp default current_timestamp  
    )
    """)
    conn.commit()
    conn.close()
def show_all(name):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(f"SELECT rowid,* FROM {name} LIMIT 2 ")
    items = c.fetchall()
    print("\n" + "=" * 120)
    print(f"{'ID':^6} | {'Number':^15} | {'Result':^8} | {'Iterations':^10} | {'Palindrome':^15} | {'Length':^8}")
    print("=" * 150)
    for item in items:
        print(f"{item[0]:^6} | {item[1]:^15} | {item[2]:^8} | {item[3]:^10} | {item[4]:^15} | {item[5]:^8} | {item[6]:^8}")
    print("=" * 150 + "\n")  
    conn.commit()
    conn.close()
def insert_row(number,result,iterations,palindrome,length,time,name):
    conn = sqlite3.connect("history.db")
    c= conn.cursor()
    c.execute(f"INSERT INTO {name} VALUES (?, ?, ?, ?, ?, ?)",(number,result,iterations,palindrome,length,time))
    conn.commit()
    conn.close()
def show_all_where(counter, name):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(f"SELECT rowid,* FROM {name} WHERE iterations >= ?", (counter,))
    items = c.fetchall()
    if not items:
        print(f"There are no numbers that required more than {counter} iterations to collapse!", file=fout)
    else:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = current_time
        if len(items) > 0:
            try:
                timestamp = items[0][6]
            except IndexError:
                pass  
                
        print(f"Documentation start time: {timestamp}\nTABLE: {name}", file=fout)
        print("=" * 150, file=fout)
        print(f"{'ID':^6} | {'Number':^18} | {'Result':^8} | {'Iterations':^10} | {'Palindrome':^50} | {'Length':^8} | {'Time':^8}", file=fout)
        print("=" * 150, file=fout)
        for item in items:
            try:
                print(f"{item[0]:^6} | {item[1]:^15} | {item[2]:^8} | {item[3]:^10} | {item[4]:^50} | {item[5]:^8} | {item[6]:^8}", file=fout)
            except IndexError:
                print(f"Error formatting item: {item}", file=fout)
        print("=" * 150 + "\n", file=fout)
        conn.commit()
    print("\n-----------------------history.db has been updated!-------------------------\n")
    conn.close()


# conn=sqlite3.connect("history.db")
# c= conn.cursor()
# c.execute(f"SELECT rowid,* FROM lychrel3 WHERE iterations > ?", (10,))
# items = c.fetchall()
# if not items:
#     print(f"There are no numbers that required more than {10} iterations to collapse!", file=fout)
# else:
#     
#     current_time = time.strftime("%Y-%m-%d %H:%M:%S")
#     timestamp = current_time
#     if len(items) > 0:
#         try:
#             
#             timestamp = items[0][6]
#         except IndexError:
#             pass  
            
#     print(f"Documentation start time: {timestamp}\nTABLE: {'lychrel3'}", file=fout)
#     print("=" * 150, file=fout)
#     print(f"{'ID':^6} | {'Number':^18} | {'Result':^8} | {'Iterations':^10} | {'Palindrome':^50} | {'Length':^8} | {'Time':^8}", file=fout)
#     print("=" * 150, file=fout)
#     for item in items:
#         try:
#             print(f"{item[0]:^6} | {item[1]:^15} | {item[2]:^8} | {item[3]:^10} | {item[4]:^50} | {item[5]:^8} | {item[6]:^8}", file=fout)
#         except IndexError:
#             print(f"Error formatting item: {item}", file=fout)
#     print("=" * 150 + "\n", file=fout)
#     conn.commit()
# print("\n-----------------------history.db has been updated!-------------------------\n")
# conn.close()

