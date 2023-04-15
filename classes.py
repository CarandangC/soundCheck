from flask import Flask, render_template, request
import sqlite3
import cartbackend

#this file houses all the classes for the website
#this file is imported into the soundCheck.py file
#it also includes the database connection for the cart database,users database, and events database 
#it mostly deals with the cart, user, and event classes and their attributes and methods

class Event:
    def __init__(self,event_name,event_date,event_time, event_location, event_price):
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        self.event_price = event_price
    
    def getinfo(self):
        return {
            "event_name": self.event_name,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "event_location": self.event_location,
            "event_price": self.event_price
        }
          
class Customer:
    def __list__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

#inherits attributes from customers cart such as event details and price. 
class Cart(Customer):
    def __init__(self, first_name, last_name, email):
        super().__init__(first_name, last_name, email)
        self.conn = sqlite3.connect('cart.db')
        self.cursor = self.conn.cursor()

    def get_cart(self):
        self.cursor.execute("SELECT event_name, event_date, event_time, event_location, event_price FROM cart")
        rows = self.cursor.fetchall()
        return rows
    
    def remove_item_from_cart(self, event_name):
        self.cursor.execute("DELETE FROM cart WHERE event_name=?", (event_name,))
        self.conn.commit()

#inherits attributes from user profile such as name and email. 
#also validates the user's password and email using the database information.        
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    
    def register(self, email, password, confirm_password):
        # Perform validation
        if not self.first_name or not self.last_name or not email or not password or not confirm_password:
            return False
        elif password != confirm_password or len(password) < 8:
            return False
        
        # Connect to the database
        db = sqlite3.connect("users.db")
        c = db.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        result = c.fetchone()

        if result is not None:
            # Delete the existing user with the same email
            c.execute("DELETE FROM users WHERE email=?", (email,))

        # Add the new user to the database
        c.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", (self.first_name, self.last_name, email, password))
        db.commit()
        db.close()
        
        return True
        
    def login(self, email, password):
        # Connect to the database
        db = sqlite3.connect("users.db")
        c = db.cursor()

        # Check if the user exists and the password is correct
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        result = c.fetchone()

        db.close()
        
        if result is not None:
            return True
        else:
            return False
        
    @staticmethod
    def validate(password, confirm_password):
        if password != confirm_password or len(password) < 8:
            return False
        else:
            return True

class Checkout_System:
    def __init__(self,name):
        self.name = name
    
#inherits attributes from checkout system such as card number, card name, cvv, expiration, and billing address.
class Verification_Process(Checkout_System):
    def __init__(self, card_number, card_name, cvv, expiration, billing_address):
        self.card_number = card_number
        self.card_name = card_name
        self.cvv = cvv
        self.expiration = expiration
        self.billing_address = billing_address
      
class Forget_Pass:
    def __init__(self,email):
        self.email = email
      
    def FORGOTPW(self):
        if not self.email:
            return render_template('forgotpw.html')
        db = sqlite3.connect('users.db')
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (self.email,))
        user = c.fetchone()
        if user is None:
            return render_template('forgotpw.html')
        c.execute("DELETE FROM users WHERE email = ?", (self.email,))
        db.commit()
        db.close()
        return render_template("soundCheck.html") 
    
class Checkout_Process(Verification_Process):
    def CHECKOUT(self):
        # Get instance variables
        card_number = self.card_number
        card_name = self.card_name
        cvv = self.cvv
        expiration = self.expiration
        billing_address = self.billing_address

        #verification process. If invalid go to cart.html (refresh the page)
        if (card_number != int and len(card_number) != 16) or (cvv != int and len(cvv) != 3) or (expiration != int and len(expiration) != 4):
            conn = sqlite3.connect('cart.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart')
            rows = cur.fetchall()
            event_list = []
            for row in rows:
                event_dict = {'name': row[0], 'date': row[1], 'time': row[2], 'location': row[3], 'price': row[4]}
                event_list.append(event_dict)
            return render_template('cart.html', events=event_list)

        if not card_name or not billing_address or not card_number or not expiration or not cvv:
            conn = sqlite3.connect('cart.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM cart')
            rows = cur.fetchall()
            event_list = []
            for row in rows:
                event_dict = {'name': row[0], 'date': row[1], 'time': row[2], 'location': row[3], 'price': row[4]}
                event_list.append(event_dict)
            return render_template('cart.html', events=event_list)#return "Error: All fields are required"
        
        else:
            #if the payment goes through put all the unique elements from the cart.db into the events.db and clear the cart.db
            conn_cart = sqlite3.connect('cart.db')
            conn_events = sqlite3.connect('events.db')

            # Get unique events from cart.db
            cur_cart = conn_cart.cursor()
            cur_cart.execute("""
                SELECT DISTINCT event_name, event_date, event_time, event_location, event_price
                FROM cart
            """)
            unique_events = cur_cart.fetchall()

            # Insert unique events into events.db
            cur_events = conn_events.cursor()
            cur_events.executemany("""
                INSERT INTO events (event_name, event_date, event_time, event_location, event_price)
                VALUES (?, ?, ?, ?, ?)
            """, unique_events)

            # Commit the changes and close the connections
            conn_events.commit()
            conn_events.close()
            conn_cart.close()

            #deletes everything in the cart (testing purposes)
            conn = sqlite3.connect('cart.db')
            c = conn.cursor()
            c.execute("DELETE FROM cart")
            conn.commit()
            conn.close()

            return render_template("purchaseConfirmed.html")