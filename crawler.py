from logic import update_orders
import time

while True:
    initial = time.time()
    update_orders()
    print('Expected wait time: ', round(time.time()-initial, 1), 's')
