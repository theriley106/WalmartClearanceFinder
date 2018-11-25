import queue
import store

class SKUQueue:
    def __init__(self, skuListLoc):
        self._skuQueue = queue.Queue()
        with open(skuListLoc) as f:
            for line in f:
                self._skuQueue.put(line[:-1])

    def pop(self):
        return self._skuQueue.get()

    def empty(self):
        return self._skuQueue.empty()

if __name__ == '__main__':
    q = SKUQueue('./MasterList1.txt')
    storeIDs = store.Store.getAllStoreNumbers()
    storeList = [ store.Store(sid) for sid in storeIDs ]
    while not q.empty():
        item = q.pop()
        for store in storeList:
            item = store.searchWalmartID(item)
            if item.format() == None:
                continue
            item.insert()
            i = item.format()
            print(i['usItemId'], i['store'], i['price'])
