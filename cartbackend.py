from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

# this .py file is for the cart page (cart.html) and the cart database (cart.db). 
# This file is for the backend of the cart page and includes the functions that add and delete items from the cart database,
# as well as the functions that display the contents of the cart database in the cart page.

app = Flask(__name__)

def CARTADD():
    event_name = request.form['event_name']
    event_date = request.form['event_date']
    event_time = request.form['event_time']
    event_location = request.form['event_location']
    event_price = request.form['event_price']

    conn = sqlite3.connect('cart.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS cart (event_name TEXT, event_date TEXT, event_time TEXT, event_location TEXT, event_price TEXT)")
    c.execute("INSERT INTO cart (event_name, event_date, event_time, event_location, event_price) VALUES (?, ?, ?, ?, ?)", (event_name, event_date, event_time, event_location, event_price))
    conn.commit()
    conn.close()

# Read the contents of the cart.db file and store them in the variable data
    conn = sqlite3.connect('cart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart")
    data = c.fetchall()
    conn.close()
    
#display what is in cart.db in the terminal (database)
    db = sqlite3.connect("cart.db")
    c = db.cursor()
    c.execute("SELECT * FROM cart")
    print(c.fetchall())    
    
# #deletes everything in the cart (testing purposes)
#     conn = sqlite3.connect('cart.db')
#     c = conn.cursor()
#     c.execute("DELETE FROM cart")
#     conn.commit()
#     conn.close()
# #deletes everything in the events.db (testing purposes)
#     conn = sqlite3.connect('events.db')
#     c = conn.cursor()
#     c.execute("DELETE FROM events")
#     conn.commit()
#     conn.close()
    return render_template("loggedIn.html")

#retrieves data
def get_events():
    conn = sqlite3.connect('cart.db')
    cur = conn.cursor()
    cur.execute("SELECT event_name, event_date, event_time, event_location, event_price FROM events")
    rows = cur.fetchall()
    return rows

