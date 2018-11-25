import json
import requests

HEADERS = json.load(open("headers.json"))
TERRAFIRM_URL = "https://www.walmart.com/terra-firma/fetch"

class Store:
    def __init__(self, storeID):
        self.storeID = storeID

    def searchWalmartID(self, wid):
        headers = HEADERS['terrafirm']
        headers['referer'] = "https://www.walmart.com/product/{}/sellers".format(wid)

        params = (('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),)
        data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(wid, self.storeID)
        res = requests.post(TERRAFIRM_URL, headers=headers, params=params, data=data)
        terrafirmaDoc = res.json()
        for key, value in terrafirmaDoc['payload']['offers'].items():
            k = terrafirmaDoc['payload']['offers'][key]
            if 'fulfillment' not in k:
                continue
            if not k['fulfillment']['pickupable']:
                continue
            price = value['pricesInfo']['priceMap']['CURRENT']['price']
            store = value['fulfillment']['pickupOptions'][0]['storeId']
            quantity = value['fulfillment']['pickupOptions'][0]["inStoreStockStatus"]
            rollback = value['pricesInfo']['priceDisplayCodes']['rollback']
            strikethrough = value['pricesInfo']['priceDisplayCodes']['strikethrough']
            reducedPrice = value['pricesInfo']['priceDisplayCodes']['reducedPrice']
            clearance = value['pricesInfo']['priceDisplayCodes']['clearance']
            storeCity = value['fulfillment']['pickupOptions'][0]['storeCity']
            storeName = value['fulfillment']['pickupOptions'][0]['storeName']
            storeAddress = value['fulfillment']['pickupOptions'][0]['storeAddress']
            storeStateOrProvinceCode = value['fulfillment']['pickupOptions'][0]['storeStateOrProvinceCode']
            storePostalCode = value['fulfillment']['pickupOptions'][0]['storePostalCode']
            availability = value['fulfillment']['pickupOptions'][0]['availability']
            productInfo = terrafirmaDoc['payload']['products']
            productInfo = productInfo[list(productInfo.keys())[0]]
            primaryProductId = productInfo['primaryProductId']
            wupc = productInfo['wupc']
            usItemId = productInfo['usItemId']
            upc = productInfo['upc']
            productType = productInfo['productType']
            longSku = productInfo['productAttributes']['sku']
            titleVal = productInfo['productAttributes']['productName']
            category = productInfo['productAttributes']['productCategory']['categoryPath']
            information = {"title": titleVal, "price": price, "rollback": rollback, "strikethrough": strikethrough, "reducedPrice": reducedPrice, "clearance": clearance, "store": store, "storeCity": storeCity, "storeName": storeName, "storeAddress": storeAddress, "storeStateOrProvinceCode": storeStateOrProvinceCode, "storePostalCode": storePostalCode, "availability": availability, "quantity": quantity, "primaryProductId": primaryProductId, "wupc": wupc, "usItemId": usItemId, "upc": upc, "productType": productType, "longSku": longSku, "category": category}
            return information
