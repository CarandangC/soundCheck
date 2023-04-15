
import os 
from app import app
import pytest
from flask import Flask, render_template, request
import tempfile
from classes import Event, Customer, Cart, User, Checkout_System, Verification_Process, Forget_Pass, Checkout_Process

def test_login():
    test_user_true = User("Jane", "Doe")
    test_user_false = User("Connie", "Hampton")
    #Check if the test_user_true is in the database or not 
    cxAccountT = ("janedoe@gmail.com", "@password123")
    cxAccountF = ("conniehampton@gmail.com", "@password123")
    assert  test_user_true.login(cxAccountT[0],cxAccountT[1]) == True
    assert test_user_false.login(cxAccountF[0],cxAccountF[1]) == False

def test_forgotPassword():
    test_user_true = Forget_Pass(str("janedoe@gmail.com"))
    test_user_false = Forget_Pass(str("conniehampton@gmail.com"))
    with app.test_request_context():
        assert test_user_true.FORGOTPW() == render_template('soundCheck.html')
        assert test_user_false.FORGOTPW() == render_template('forgotpw.html')
   
def test_register():
    test_user_true = User("Jane", "Doe")
    test_user_false = User("Connie", "Hampton")
    cxRegT = ("janedoe@gmail.com", "@password123", "@password123")
    cxRegF = ("conniehampton@gmail.com", "@password123", "@Password123")
    assert test_user_true.register(cxRegT[0], cxRegT[1], cxRegT[2]) == True
    assert test_user_false.register(cxRegT[0], cxRegF[1], cxRegF[2]) == False

def test_cart():
    test_true = Verification_Process(4520963845162359, "Jane Doe", 266, 1125, "12 Fawndale Ave")
    test_false= Verification_Process(452096384517835, "Connie Hampton", 246, 1127, "12 Fawndale Ave")
    t_t = Checkout_Process("4520963845162359", "Jane Doe", "266", "1125", "12 Fawndale Ave")
    t_f = Checkout_Process("", "Connie Hampton", "246", "1127", "12 Fawndale Ave")
    with app.test_request_context():
        assert t_t.CHECKOUT() == render_template('purchaseConfirmed.html')
        assert t_f.CHECKOUT() == render_template('cart.html')


    