'''Accesses Gemini Api'''

import time
import json
import requests
import base64
import hmac
from hashlib import sha384

#maximum 600 calls per minute and 5 calls per second
class Gemini:
    url = 'https://api.sandbox.gemini.com/'
    API_KEY_PUBLIC = '8vOMHNqIBidi28arpoYY'
    API_KEY_PRIVATE = '8A19TT8juVSuBeMW8E2NbpXey7x'

    def nonce(self):
        return str(time.time())

    def generate_headers(self, parameters=None):
        #encode parameters in json
        parameters = json.dumps(parameters)

        #then encode as base64
        payload = base64.b64encode(parameters.encode())

        #create a signature
        signature = hmac.new(self.API_KEY_PRIVATE.encode(), payload, sha384).hexdigest()

        #default headers
        headers = {
                    'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': self.API_KEY_PUBLIC,
                    'X-GEMINI-PAYLOAD': payload,
                    'X-GEMINI-SIGNATURE': signature,
                    'Cache-Control': "no-cache"
                    }


        return headers

    def check_order(self, order_id):
        parameters = {
                    'request': '/v1/order/status',
                    'nonce': self.nonce(),
                    'order_id': str(order_id),
                    }

        headers = self.generate_headers(parameters)

        r = requests.post(self.url + '/v1/order/status', headers=headers)

        return r.json()

    def cancel_order(self, order_id):
        parameters = {
                    'request': '/v1/order/cancel',
                    'nonce': self.nonce(),
                    'order_id': order_id,
                    }

        headers = self.generate_headers(parameters)

        with requests.post(self.url + '/v1/order/cancel', headers=headers) as r:
            return r.json()

    #make a order given a dictionary
    def order(self, kargs):
        parameters = {'request': '/v1/order/new', 'nonce': str(time.time())}
        parameters.update(kargs)

        headers = self.generate_headers(parameters)

        #create the order
        response = requests.post(self.url + '/v1/order/new', headers=headers)

        return response.json()['order_id']


#grabs quote
def get_quote(ticker):
    data = requests.get('https://api.sandbox.gemini.com/v1/pubticker/' + ticker).json()
    return data
