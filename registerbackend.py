from flask import Flask, render_template, request, redirect, url_for
from classes import User
import sqlite3

#If the user creates a profile successfully on the register page, 
#redirect them into the login page where they can log in.
    
def REGISTER():
    # Retrieve the registration data from the form
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    
    # Return a response to the user
    user_instance = User(first_name, last_name)
    if not user_instance.register(email, password, confirm_password):
        return render_template("register.html")
    else:
        #if it is true, then it has already registered the user
        
    #display what is in users.db in the terminal (database) 
        db = sqlite3.connect("users.db")
        c = db.cursor()
        c.execute("SELECT * FROM users")
        print(c.fetchall())    
        return render_template("login.html") #return "Success: User added to the database"
