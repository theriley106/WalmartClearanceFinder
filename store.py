import json
import csv
import requests

HEADERS = json.load(open("headers.json"))
TERRAFIRM_URL = "https://www.walmart.com/terra-firma/fetch"

class Item:
    def __init__(self, itemJSON):
        terrafirmaDoc = itemJSON
        for key, value in terrafirmaDoc['payload']['offers'].items():
            try:
                k = terrafirmaDoc['payload']['offers'][key]
                self.price = value['pricesInfo']['priceMap']['CURRENT']['price']
                self.store = value['fulfillment']['pickupOptions'][0]['storeId']
                self.quantity = value['fulfillment']['pickupOptions'][0]["inStoreStockStatus"]
                self.rollback = value['pricesInfo']['priceDisplayCodes']['rollback']
                self.strikethrough = value['pricesInfo']['priceDisplayCodes']['strikethrough']
                self.reducedPrice = value['pricesInfo']['priceDisplayCodes']['reducedPrice']
                self.clearance = value['pricesInfo']['priceDisplayCodes']['clearance']
                self.storeCity = value['fulfillment']['pickupOptions'][0]['storeCity']
                self.storeName = value['fulfillment']['pickupOptions'][0]['storeName']
                self.storeAddress = value['fulfillment']['pickupOptions'][0]['storeAddress']
                self.storeStateOrProvinceCode = value['fulfillment']['pickupOptions'][0]['storeStateOrProvinceCode']
                self.storePostalCode = value['fulfillment']['pickupOptions'][0]['storePostalCode']
                self.availability = value['fulfillment']['pickupOptions'][0]['availability']

                productInfo = terrafirmaDoc['payload']['products']
                productInfo = productInfo[list(productInfo.keys())[0]]
                self.primaryProductId = productInfo['primaryProductId']
                self.usItemId = productInfo['usItemId']
                self.upc = productInfo['upc']
                self.productType = productInfo['productType']
                self.longSku = productInfo['productAttributes']['sku']
                self.name = productInfo['productAttributes']['productName']
                self.category = productInfo['productAttributes']['productCategory']['categoryPath']
                self.hasItem = True
                return
            except:
                self.hasItem = False

    def format(self):
        if not self.hasItem:
            return None
        return {
            "name":                         self.name,
            "price":                        self.price,
            "rollback":                     self.rollback,
            "strikethrough":                self.strikethrough,
            "reducedPrice":                 self.reducedPrice,
            "clearance":                    self.clearance,
            "store":                        self.store,
            "storeCity":                    self.storeCity,
            "storeName":                    self.storeName,
            "storeAddress":                 self.storeAddress,
            "storeStateOrProvinceCode":     self.storeStateOrProvinceCode,
            "storePostalCode":              self.storePostalCode,
            "availability":                 self.availability,
            "quantity":                     self.quantity,
            "primaryProductId":             self.primaryProductId,
            "usItemId":                     self.usItemId,
            "upc":                          self.upc,
            "productType":                  self.productType,
            "longSku":                      self.longSku,
            "category":                     self.category
        }

class Store:
    def __init__(self, storeID):
        self._storeID = storeID

    @staticmethod
    def getAllStoreNumbers():
        print('Short circuit store numbers')
        return [1123]
        def isSupercenter(name):
            return 'Walmart Supercenter' in name
        walmartFile = open('Walmarts.csv')
        walmarts = list(csv.reader(walmartFile))
        walmartFile.close()
        walmarts = [ w[0] for w in walmarts if isSupercenter(w[1]) ]
        return walmarts

    def searchWalmartID(self, wid):
        headers = HEADERS['terrafirm']
        headers['referer'] = "https://www.walmart.com/product/{}/sellers".format(wid)

        params = (('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),)
        data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(wid, self._storeID)
        res = requests.post(TERRAFIRM_URL, headers=headers, params=params, data=data)
        return Item(res.json())
