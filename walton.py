import sys
import argparse
import store
import time
import queue
import itertools
from multiprocessing.pool import ThreadPool
import psycopg2

total = 0
count = 0

conn = psycopg2.connect("dbname=wolfofwalmart user=postgres host=192.168.1.120 password=password123!!!")

class SKUQueue(): 
    def __init__(self, skuListLoc):
        self._skuQueue = queue.Queue()
        with open(skuListLoc) as f:
            for line in f:
                self._skuQueue.put(line[:-1])

    def __iter__(self):
        while not self._skuQueue.empty():
            yield self._skuQueue.get()

def createTable():
    cur = conn.cursor()
    cur.execute('''
CREATE TABLE IF NOT EXISTS skus(
    id INTEGER,
    store_id INTEGER,
    quantity TEXT,
    title TEXT,
    category TEXT,
    price MONEY,
    store_city TEXT,
    store_name TEXT,
    PRIMARY KEY(id, store_id)
);''')
    conn.commit()
    cur.close()

def dropTable():
    cur = conn.cursor()
    cur.execute('DROP TABLE skus')
    conn.commit()
    cur.close()
    

def insert(item):
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO skus VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (item['usItemId'], item['store'], item['quantity'], item['name'], item['category'], item['price'], item['storeCity'], item['storeName']))
        conn.commit()
        cur.close()
    except:
        pass

def searchAndInsert(args):
    global count
    count += 1
    print('%s/%s' % (count, total))
    store, itemID = args
    item = store.searchWalmartID(itemID)
    if item.format() == None:
        return None
    i = item.format()
    itemID, store, price = i['usItemId'], i['store'], i['price']
    insert(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t','--threads', help='Specify thread count', required=False, default=60)
    parser.add_argument('-s','--store', nargs='+', help='Store IDs', required=True, default=[])
    parser.add_argument('--drop', action='store_true', help='Drop Database for new data', required=False)
    args = vars(parser.parse_args())
    
    print('Using %d threads' % args['threads'])

    # if args['drop']:
    #     dropTable()
    #     sys.exit()

    createTable()
    print('Created table')
    q = SKUQueue('./MasterList.txt')
    storeIDs = args['store']
    storeList = [ store.Store(sid) for sid in storeIDs ]

    productStoreList = itertools.product(storeList, q)
    total = len(productStoreList)
    with ThreadPool(args['threads']) as p:
        p.map(searchAndInsert, productStoreList)
    conn.close()
