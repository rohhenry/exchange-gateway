import gemini
import db
import time

class OrderParameters:
    def __init__(self, session, form):
        self.username = session['username']
        self.password = session['password']
        self.option = form['option']
        self.price = float(form['price'])
        self.eth_amount = float(form['amount'])
        self.usd_amount = self.eth_amount * self.price

#given a request form determine whether it is a valid request
def is_order_valid(session, form):
    order = OrderParameters(session, form)

    if not db.authenticate(order.username, order.password):
        return 'BAD USERNAME OR PASSWORD'

    order.usd_balance, order.eth_balance = db.get_balance(order.username)

    #user wants to purchase eth
    if order.option == 'buy' and order.usd_amount > order.usd_balance:
        return 'NOT ENOUGH USD'

    #user wants to sell eth
    elif order.option == 'sell' and order.eth_amount > order.eth_balance:
        return 'NOT ENOUGH ETH'

    return order

def make_order(order):

    info = {
            'symbol': 'ethusd',
            'type': 'exchange limit'
            }

    info['side'] = order.option
    info['amount'] = order.eth_amount
    info['price'] = order.price

    handle = gemini.Gemini()

    #do order
    order_id = handle.order(info)

    if order.option == 'buy':
        db.edit_orders(order.username, order_id, 'buy', -1 * order.usd_amount, order.eth_amount)
        db.edit_balance(order.username, -1 * order.usd_amount, 0)
    elif order.option == 'sell':
        db.edit_orders(order.username, order_id, 'sell', order.usd_amount, -1 * order.eth_amount)
        db.edit_balance(order.username, 0, -1 * order.eth_amount)

#attempts to revert a transaction if possible
'''def revert_transaction(order_id):
    handle = gemini.Gemini()
    info = handle.order_status(order_id)

    if info['is_cancelled'] is True:
        return 'Already Cancelled'
    if info['is_live'] is False:
        return 'Order Already Filled'

    info = handle.cancel_order():

    refund_eth_amount = info['remaining_amount']
    refund_usd_amount = info['remaining_amount'] * info['price']

    if info['side'] =='buy':
'''

def update_orders():
    orders = db.get_orders()
    handle = gemini.Gemini()
    for order in orders:
        data = handle.check_order(order[1])
        if data['is_live'] == False:
            db.edit_transaction(*order)
            db.delete_order(order[1])
            if order[2] == 'buy':
                db.edit_balance(order[0], 0, order[4])
            elif order[2] == 'sell':
                db.edit_balance(order[0], order[4], 0)
            print('Processed: ', order[1])
        time.sleep(0.1)
