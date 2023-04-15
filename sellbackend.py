from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# this .py file is the backend for sell.html (the form for selling tickets) and sell.html is the frontend for this .py file (the backend) 
# it will be used to create a new event in the database and save that event to the database (events.db) as well as display the contents of the database in the terminal.

def SELL():
    event_name = request.form["eventName"]
    event_date = request.form["date"]
    event_time = request.form["time"]
    event_location = request.form["location"]
    event_price = request.form["price"]
    artist_img = request.form["artistImg"]
    
    
    # Save form data to database
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (name, date, time, location, price, image) VALUES (?, ?, ?, ?, ?, ?)',
              (event_name, event_date, event_time, event_location, event_price, artist_img))
    conn.commit()
    conn.close()
    
    #display what is in events.db in the terminal (database)
    db = sqlite3.connect("events.db")
    c = db.cursor()
    c.execute("SELECT * FROM events")
    print(c.fetchall())    
    return #Event successfully created and sold!

