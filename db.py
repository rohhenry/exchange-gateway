'''Performs on Database'''

import sqlite3
import os

def restart():
    os.remove('info.db')

    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    c.execute('''CREATE TABLE info (username text, password text, usd_balance real, eth_balance real)''')

    c.execute('''CREATE TABLE transactions (username text, order_id text, option text, usd_amount real, eth_amount real)''')

    c.execute('''CREATE TABLE orders (username text, order_id text, option text, usd_amount real, eth_amount real)''')

    c.execute("INSERT INTO info VALUES ('t0ska', 'password', '100000', '0')")

    conn.commit()

    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    credentials = username, password

    c.execute("SELECT * FROM info WHERE username=? AND password=? LIMIT 1", credentials)

    if not c.fetchone():
        conn.close()
        return False

    conn.close()
    return True

def get_balance(username):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    credentials = username,

    c.execute("SELECT usd_balance, eth_balance FROM info WHERE username=? LIMIT 1", credentials)

    return c.fetchone()

def edit_balance(username, usd_amount, eth_amount):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    current_balance = get_balance(username)

    new_usd_balance = current_balance[0] + float(usd_amount)
    new_eth_balance = current_balance[1] + float(eth_amount)

    arguments = new_usd_balance, new_eth_balance, username

    c.execute("UPDATE info SET usd_balance=?, eth_balance=? WHERE username=?", arguments)

    conn.commit()

    conn.close()

    return True

def new_user(username, password):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    arguments = username,

    c.execute("SELECT username FROM info WHERE username=?", arguments)

    if c.fetchone():
        return False

    arguments = username, password

    c.execute("INSERT INTO info VALUES (?, ?, 0, 0)", arguments)

    conn.commit()

    conn.close()

    return True

def edit_transaction(username, order_id, buy, usd_amount, eth_amount):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    arguments = username, order_id, buy, usd_amount, eth_amount

    c.execute("INSERT INTO transactions VALUES (?,?,?,?,?)", arguments)

    conn.commit()

    conn.close()

    return True

def get_transactions(username):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    arguments = username,

    c.execute("SELECT * FROM transactions WHERE username=?", arguments)

    return c.fetchall()

def edit_orders(username, order_id, buy, usd_amount, eth_amount):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    arguments = username, order_id, buy, usd_amount, eth_amount

    c.execute("INSERT INTO orders VALUES (?,?,?,?,?)", arguments)

    conn.commit()

    conn.close()

    return True

def get_orders(*args):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    if args:
        c.execute("SELECT * FROM orders WHERE username=?", args)
    else:
        c.execute("SELECT * FROM orders")

    return c.fetchall()

def delete_order(order_id):
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    c.execute("DELETE FROM orders WHERE order_id=?", (order_id,))

    conn.commit()

    conn.close()

    return True

def delete_all_orders():
    conn = sqlite3.connect('info.db')

    c = conn.cursor()

    c.execute("DELETE FROM orders")

    conn.commit()

    conn.close()

    return True
