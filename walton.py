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
    id TEXT,
    store_id INTEGER,
    quantity TEXT,
    title TEXT,
    category TEXT,
    price MONEY
);''')
    conn.commit()
    cur.close()

def insert(item):
    cur = conn.cursor()
    cur.execute('INSERT INTO skus VALUES(%s, %s, %s, %s, %s, %s)', (item['usItemId'], item['store'], item['quantity'], item['name'], item['category'], item['price']))
    conn.commit()
    cur.close()

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
    print(itemID, store, price)
    insert(i)

if __name__ == '__main__':
    createTable()
    q = SKUQueue('./MasterList.txt')
    total = q._skuQueue.qsize()
    storeIDs = store.Store.getAllStoreNumbers()
    storeList = [ store.Store(sid) for sid in storeIDs ]

    productStoreList = itertools.product(storeList, q)
    with ThreadPool(60) as p:
        p.map(searchAndInsert, productStoreList)
    conn.close()
