'''The Actual WebApp... super ugly and messy right now I will abstract it away'''
from flask import Flask, request, session, redirect
import logic
import gemini
import db

app = Flask(__name__)
app.secret_key = 'asdjflskajdkjlasfjlksdfaklsdfa'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not db.authenticate(request.form['username'], request.form['password']):
            return 'Incorrect Username or Password'

        session['username'] = request.form['username']
        session['password'] = request.form['password']

        return redirect('/balance')
    elif request.method == 'GET':
        with open('login.html', 'r') as f:
            return f.read()

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/login')

@app.route('/order', methods=['GET','POST'])
def form():
    if request.method == 'POST':
        order = logic.is_order_valid(session, request.form)

        if isinstance(order, str):
            return order
        logic.make_order(order)
        with open('links.html', 'r') as l:
            return redirect('/orders')
    else:
        with open('order.html', 'r') as f:
            return '{}{}'.format(
                                '<h1>Current Price: ' + gemini.get_quote('ethusd')['last'] + ' ETH/USD</h1>',
                                f.read()
                                )

'''@app.route('/cancel', methods=['GET','POST'])
def cancel():
    if request.method == 'POST':
        with open('links.html','r') as c:
            return logic.revert_transaction(session, form.method['order_id']) + c.read()
    if request.method == 'GET':
        with open('cancel.html') as c:
            return c.read()'''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not db.new_user(request.form['username'], request.form['password']):
            return 'Username {} Taken'.format(request.form['username'])
        db.edit_balance(request.form['username'], 10000, 100)
        return redirect('/login')
    elif request.method == 'GET':
        with open('signup.html', 'r') as f:
            return f.read()

@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'GET':
        usd_balance, eth_balance = db.get_balance(session['username'])
        with open('links.html', 'r') as l:
            return 'USD: {} ETH: {}{}'.format(usd_balance, eth_balance, l.read())

@app.route('/transactions', methods=['GET'])
def transactions():
    with open('links.html', 'r') as l:
        return '<h1>Transaction History</h1><p>username, order_id, option, complete, usd_value, eth_value</p>{}{}'.format(db.get_transactions(session['username']), l.read())

@app.route('/orders', methods=['GET'])
def orders():
    with open('links.html', 'r') as l:
        return '<h1>Open Orders</h1><p>username, order_id, option, complete, usd_value, eth_value</p>{}{}'.format(db.get_orders (session['username']), l.read())
