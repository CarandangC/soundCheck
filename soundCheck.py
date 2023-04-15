from flask import Flask, render_template, request
import sqlite3 
import json
import registerbackend, loginbackend, checkoutbackend, forgetpwbackend, cartbackend

#this is the backend of the main page of the website. it reads the databases and returns the relevant .html pages with the matching information from their respective databases on it 
#all the routes for the different pages on the website. reads the url and returns the correct html file
#there are also certain routes that are called when a button is pressed on the html page. these routes are called in the html file and are defined here in the main python file

app = Flask(__name__)
# #deletes everything in the users database (testing purposes)
# db = sqlite3.connect("users.db")
# c = db.cursor()
# c.execute("DELETE FROM users")
# db.commit()
# db.close()

# #deletes everything in the cart (testing purposes)
# conn = sqlite3.connect('cart.db')
# c = conn.cursor()
# c.execute("DELETE FROM cart")
# conn.commit()
# conn.close()

# #deletes everything in the events (testing purposes)
# conn = sqlite3.connect('events.db')
# c = conn.cursor()
# c.execute("DELETE FROM events")
# conn.commit()
# conn.close()

@app.route('/')
def home():
        return render_template("soundCheck.html")

@app.route('/soundCheck')
def soundCheck():
        return render_template("soundCheck.html")
    
@app.route('/login')
def login():
        return render_template("login.html")

@app.route('/loggedIn')
def loggedin():
        return render_template("loggedin.html")

@app.route('/register')
def register():
    return render_template("register.html")

#this route is called when the user presses the evnts button on the main page. it reads the events.db database and returns the events.html page with the events from the database on it
#this is the same for the cart route
@app.route('/events')
def events():
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT * FROM events')
    rows = cur.fetchall()
    event_list = []
    for row in rows:
        event_dict = {'name': row[0], 'date': row[1], 'time': row[2], 'location': row[3], 'price': row[4]}
        event_list.append(event_dict)
    return render_template('events.html', events=event_list)

@app.route('/cart')
def cart():
    conn = sqlite3.connect('cart.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cart')
    rows = cur.fetchall()
    event_list = []
    for row in rows:
        event_dict = {'name': row[0], 'date': row[1], 'time': row[2], 'location': row[3], 'price': row[4]}
        event_list.append(event_dict)
    return render_template('cart.html', events=event_list)
    
@app.route('/customerFAQ')
def customerfaq():
        return render_template("customerFAQ.html")

@app.route('/loggedFAQ')
def loggedfaq():
        return render_template("loggedInFAQ.html")

@app.route('/contact')
def contact():
        return render_template("contact.html")

@app.route('/loggedContact')
def loggedContact():
        return render_template("loggedInContact.html")
    
@app.route('/forgotpw')
def forgotpw():
        return render_template("forgotpw.html")

#this is the function to create a database for the users. it creates a database called users.db and a table called users
def create_db():
    db = sqlite3.connect("users.db")
    c = db.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, password TEXT, confirm_password TEXT)")
    db.commit()
    db.close()

@app.route("/REGISTER", methods=["POST"])
#call the function REGISTER from registerbackend.py
def registerconfirm():
        return registerbackend.REGISTER()

@app.route("/LOGIN", methods=["POST"])
#call the function LOGIN from loginbackend.py
def loginconfirm():
        return loginbackend.LOGIN()

@app.route("/CART", methods=["POST"])
#call the function SELL from cartbackend.py
def cartconfirm():
        return checkoutbackend.CHECKOUT()

#this route is called when the user pressed the add to cart button on the main page
@app.route("/add-to-cart", methods=["POST"])
def addtocart():
        return cartbackend.CARTADD()

@app.route("/FORGOTPW", methods=["POST"])
def forgotpwconfirm():
        return forgetpwbackend.FORGOTPW()

@app.route('/purchaseConfirmed')
def purchaseconfirmed():
        return render_template("purchaseConfirmed.html")

#generate the local ip address and run the website on the local ip address. displays it in the terminal
if __name__ == '__main__':
    app.run(debug=True)