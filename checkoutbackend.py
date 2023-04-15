from flask import Flask, render_template, request, redirect, url_for
import sqlite3, cartbackend, os
from classes import Checkout_Process

# Create a connection to the database and requests card information

def CHECKOUT():
    card_number = request.form["cardNumber"]
    card_name = request.form["cardName"]
    cvv = request.form["cvv"]
    expiration = request.form["expiryDate"]
    billing_address = request.form["billingAddress"]
    
    confirmation = Checkout_Process(card_number, card_name, cvv, expiration, billing_address)
    return confirmation.CHECKOUT()
