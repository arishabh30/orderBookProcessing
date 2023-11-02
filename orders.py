import xml.etree.ElementTree as ET
from collections import defaultdict
import time
from datetime import datetime


# Creating dictionaries to store buy and sell order books
buy_order_books = defaultdict(list)
sell_order_books = defaultdict(list)


# To process the AddOrder condtition
def process_add_order(add_order):
    book = add_order.get('book')
    operation = add_order.get('operation')
    price = float(add_order.get('price'))
    volume = int(add_order.get('volume'))
    order_id = int(add_order.get('orderId'))

    insert_order(book, operation, price, volume, order_id)
    

# To insert an order into the book 
def insert_order(book, operation, price, volume, order_id):
    i = 0

    if operation == "BUY" :
        while i < len(sell_order_books[book]) :
            existing_order = sell_order_books[book][i]
            if ((existing_order['price'] <= price) and existing_order['order_id'] < order_id):
                min_vol = min(volume, existing_order['volume'])
                sell_order_books[book][i]['volume'] = existing_order['volume'] - min_vol
                if(sell_order_books[book][i]['volume'] == 0) :
                    sell_order_books[book].pop(i)
                volume = volume- min_vol
            i += 1
        if volume != 0:
            buy_order_books[book].insert(i, {'price' : price, 'volume' : volume, 'order_id' : order_id})
            buy_order_books[book].sort(key=lambda a : a['order_id'])
            buy_order_books[book].sort(key=lambda a : a['price'], reverse=True)
    else :
        while i < len(buy_order_books[book]) :
            existing_order = buy_order_books[book][i]
            if ((existing_order['price'] >= price) and existing_order['order_id'] < order_id):
                min_vol = min(volume, existing_order['volume'])
                buy_order_books[book][i]['volume'] = existing_order['volume'] - min_vol
                if(buy_order_books[book][i]['volume'] == 0) :
                    buy_order_books[book].pop(i)
                volume = volume- min_vol
            i += 1

        if volume != 0 :
            sell_order_books[book].insert(i, {'price' : price, 'volume' : volume, 'order_id' : order_id})
            sell_order_books[book].sort(key=lambda a : a['order_id'])
            sell_order_books[book].sort(key=lambda a : a['price'], reverse=False)


# To process a DeleteOrder message
def process_delete_order(delete_order):
    book = delete_order.get('book')
    order_id = int(delete_order.get('orderId'))

    buy_order_book = buy_order_books[book]
    sell_order_book = sell_order_books[book]

    remove_order(buy_order_book, order_id)
    remove_order(sell_order_book, order_id)


# To remove an order
def remove_order(order_book, order_id):
    for order in order_book:
        # print("Order : ",order['order_id'])
        # print("Condition: ", order['order_id'] == order_id)
        if order['order_id'] == order_id:
            order_book.remove(order)
            return


# To print the order books
def print_order_books():
    print("Order Books:")
    for book, buy_orders in buy_order_books.items():
        sell_orders = sell_order_books[book]
        print(book)
        print("Buy")
        for order in buy_orders:
            print(f"{order['volume']} @ {order['price']:.2f}")
        print("Sell")
        for order in sell_orders:
            print(f"{order['volume']} @ {order['price']:.2f}")

# Parsing the XML file
tree = ET.parse('orders.xml')
root = tree.getroot()

start_time = time.time()

for message in root:
    if message.tag == 'AddOrder':
        process_add_order(message)
    elif message.tag == 'DeleteOrder':
        process_delete_order(message)


end_time = time.time()

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
print(f"Processing started at: {current_time}")

print_order_books()

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
print(f"Processing finished at: {current_time}")
print(f"Processing Duration (seconds): {end_time - start_time}")
