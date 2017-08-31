from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
from sqlalchemy.orm import sessionmaker
from app import app
from app import db, models
from .models import User, Server
import requests
import simplejson
import json
from babel import Locale
import babel.numbers
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
import decimal
import string
# from .forms import LoginForm, EditForm, PostForm
from config import POSTS_PER_PAGE, prodURLDefault

locale = Locale('en', 'US')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        return render_template('index.html')



@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    s = db.session
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
        userValues = s.query(User).filter_by(username=POST_USERNAME).first()
        lookServer = s.query(Server).filter_by(envName=userValues.useEnv).first()
        session['username'] = POST_USERNAME
        session['apiKey'] = userValues.apiKey
        session['accountID'] = lookServer.accountID
        if userValues.useEnv != "":
            serverValues = s.query(Server).filter_by(envName=userValues.useEnv).first()
            session['prodURL'] = serverValues.prodURL
        else:
            session['prodURL'] = prodURLDefault

    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    greet = "Anonymous"
    return home()


@app.route('/test')
def test():
    POST_USERNAME = "admin"
    POST_PASSWORD = "TimIsGod"

    s = db.session
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD


@app.route('/products')
def goProducts():
    uri = session['prodURL']+"/billing/2/products"
    headerAPI = session['apiKey']
    try:
        uResponse = requests.get(uri, headers={"x-api-key": headerAPI})
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    productName = data[0]['name']  # <-- The product name
    productType = data[0]['product_type']  # <-- The product type
    productID = data[0]['id']  # <-- The product ID

    return render_template('products.html', **locals())


@app.route('/account')
def goAccount():
    uri = session['prodURL']+"/billing/2/billing-accounts/"+session['accountID']
    headerAPI = session['apiKey']
    try:
        uResponse = requests.get(uri, headers={"x-api-key": headerAPI})
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    actNum = data['account_num']  # <-- The TRACT Account Number
    actStatus = data['status']  # <-- TRACT Account Status

    if not data['currency_code']:
        currencyCode = "USD"
    else:
        currencyCode = data['currency_code']
    #print(currencyCode)
    actCharges = babel.numbers.format_currency(data['pending_charges_total'], currencyCode, locale=locale)  # <-- Total Pending Charges in Currency code
    d = datetime.strptime(data['next_invoice_date'], "%Y-%m-%dT%H:%M:%S.%f%z")
    nxtInvoiceDate = format_date(d, format='full', locale='en')
    #nxtInvoiceDate = data['next_invoice_date']
    print(data)
    #return "Look at print"
    return render_template('account.html', **locals())


@app.route('/invoices')
def goInvoices():
    uri = session['prodURL']+"/billing/2/invoices?billing_account_id="+session['accountID']
    headerAPI = session['apiKey']
    try:
        uResponse = requests.get(uri, headers={"x-api-key": headerAPI})
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    return render_template('invoice_list.html', **locals())

@app.route('/invoice_detail', methods=['POST'])
def goInvoiceDetail():
    data_posted = request.form
    uri = session['prodURL']+"/billing/2/invoices?billing_account_id="+session['accountID']+"&id="+data_posted['id']
    headerAPI = session['apiKey']
    try:
        uResponse = requests.get(uri, headers={"x-api-key": headerAPI})
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    return render_template('invoices.html', **locals())

@app.route('/profile', methods=['GET', 'POST'])
def goProfile():
    s = db.session
    if request.method == 'POST':
            data_posted = request.form
            profile = s.query(User).filter_by(username=session['username']).first()
            lookServer = s.query(Server).filter_by(envName=data_posted['useEnv']).first()
            profile.email = data_posted['email']
            profile.apiKey = data_posted['apiKey']
            profile.useEnv = data_posted['useEnv']
            profile.accountID = lookServer.accountID
            profile.apiKey = lookServer.apiKey
            profile.password = data_posted['password']
            s.commit()

            return logout()
    else:
            print("Get Executed")
            userValues = s.query(User).filter_by(username=session['username']).first()
            lookServer = s.query(Server).filter_by(envName=userValues.useEnv).first()
            envValues = s.query(Server.envName).distinct()

            return render_template('profile.html', **locals())

@app.route('/about')
def goAbout():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # if not greet:
        return render_template('about.html')


@app.route('/account_addresses', methods=['GET', 'POST'])
def run_get_account_test():
    if request.method == 'POST':
        url_base = session['prodURL']+"/billing/2/people/"
        data_posted = request.form
        url_add = data_posted['responsible_id']+"/addresses"
        url = url_base + url_add
        headerAPI = session['apiKey']
        headers = {'Content-Type': 'application/json', 'x-api-key': headerAPI}
        r = json.dumps(data_posted)
        #print(url)
        #print(r)
        makePost = requests.post(url, data=json.dumps(data_posted), headers=headers)
        #print("-------------json sent------------")
        #print(json.dumps(makePost.json()))
        url_get = session['prodURL']+"/billing/2/billing-accounts/"+session['accountID']
        r = requests.get(url_get, headers={"x-api-key": headerAPI})
        JResponse = r.text
        data = json.loads(JResponse)

        actNum = data['account_num']  # <-- The TRACT Account Number
        actStatus = data['status']  # <-- TRACT Account Status
        actCharges = babel.numbers.format_currency(data['pending_charges_total'],
                                                   data['currency_code'], locale=locale)  # <-- Total Pending Charges in Currency code
        d = datetime.strptime(data['next_invoice_date'], "%Y-%m-%dT%H:%M:%S.%f%z")
        nxtInvoiceDate = format_date(d, format='full', locale='en')
        # nxtInvoiceDate = data['next_invoice_date']
        print(data)
        # return "Look at print"
        for item in data["responsible_party"]["addresses"]:
            if item["address_type"] == "postal":
                print(item["address_type"])

        return render_template('account2.html', **locals())
    else:
        uri = session['prodURL']+"/billing/2/billing-accounts/"+session['accountID']
        headerAPI = session['apiKey']

        # this issues a GET to the url. replace "get" with "post", "head",
        # "put", "patch"... to make a request using a different method
        try:
            uResponse = requests.get(uri, headers={"x-api-key": headerAPI})
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        data = json.loads(Jresponse)

        actNum = data['account_num']  # <-- The TRACT Account Number
        actStatus = data['status']  # <-- The product type
        actCharges = data['pending_charges_total']  # <-- The product ID

        for item in data["responsible_party"]["addresses"]:
            if item["address_type"] == "postal":
                print(item["address_type"])

        return render_template('account2.html', **locals())

@app.route('/admin', methods=['GET', 'POST'])
def goAdmin():
    s = db.session
    if request.method == 'POST':
            data_posted = request.form
            serverUpdate = s.query(Server).filter_by(envName=data_posted['envName']).first()
            serverUpdate.envName = data_posted['envName']
            serverUpdate.apiKey = data_posted['apiKey']
            serverUpdate.accountID = data_posted['accountID']
            serverUpdate.prodURL = data_posted['prodURL']
            s.commit()

            #serverValues = s.query(Server).order_by(Server.envName).all()
            #return render_template('admin.html', **locals())

            return logout()
    else:
            serverValues = s.query(Server).order_by(Server.envName).all()
            print(serverValues)

            return render_template('admin.html', **locals())