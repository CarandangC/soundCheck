from flask import Flask, render_template, request
import sqlite3


# Define a route to handle the forgot password request
#if the email is in the database, it removes that account from the database and the user has to create a new account
#if the email is not in the database, it refreshes the page

def FORGOTPW():
    email = request.form.get('email')
    if not email:
        return render_template('forgotpw.html')
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    if user is None:
        return render_template('forgotpw.html')
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    db.commit()
    db.close()
    return render_template("soundCheck.html")
