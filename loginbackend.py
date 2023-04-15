from flask import Flask, render_template, request, redirect, url_for
from classes import User
import sqlite3

"""_summary_
    Takes email and password given by the user and checks if it is in the database.
    If it is in the database and the correct credentials has been provided then redirect them to the main page.
    If not redirect them to the login page (refresh the page)
"""

def LOGIN():
    if request.method == "POST":
        # Retrieve the login data from the form
        email = request.form["email"]
        password = request.form["password"]
    
    user = User("", "") # Create a User object with empty first and last names
    if user.login(email, password):
        # If the email and password are in the database, redirect to the home page
        return render_template("loggedin.html")
    else:
        # If the email and password are NOT in the database, refresh the page
        return render_template("login.html", error="Invalid email or password")