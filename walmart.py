import requests
import json
import headers
import time
import csv
VERBOSE = 0
REQUEST_TIMEOUT = 10
NETWORK_RETRY = 3
PAUSE_BETWEEN_REQUESTS = 0
# This is the short pause between consequetive network requests

TERRAFIRM_URL = "https://www.walmart.com/terra-firma/fetch"

class Hasher(dict):
    # https://stackoverflow.com/a/3405143/190597
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def network_request(url, headers, post=False, params=None, timeout=None, data=None, network_retry=None):
	# This is the function that makes network requests
	if network_retry == None:
		# Sets params to default
		network_retry = NETWORK_RETRY
	if timeout == None:
		# Sets params to default
		timeout = REQUEST_TIMEOUT
	for _ in range(network_retry):
		if post:
			res = requests.post(url, headers=headers, params=params, data=data, timeout=timeout)
		else:
			res = requests.get(url, headers=headers, params=params, data=data, timeout=timeout)
		# Makes the network request
		if res != None:
			if res.status_code == 200:
				# This means it was successful
				return res
		time.sleep(PAUSE_BETWEEN_REQUESTS)
		# Pause to prevent back to back requests


def returnPricing(terrafirmaDoc):
	# Extracts pricing information from the terrafirm API response
	terrafirmaDoc = Hasher(terrafirmaDoc)
	for key, value in terrafirmaDoc['payload']['offers'].items():
		try:
			price = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceMap']['CURRENT']['price']
			store = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeId']
			quantity = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]["inStoreStockStatus"]
			rollback = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceDisplayCodes']['rollback']
			strikethrough = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceDisplayCodes']['strikethrough']
			reducedPrice = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceDisplayCodes']['reducedPrice']
			clearance = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceDisplayCodes']['clearance']
			storeCity = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeCity']
			storeName = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeName']
			storeAddress = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeAddress']
			storeStateOrProvinceCode = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeStateOrProvinceCode']
			storePostalCode = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storePostalCode']
			availability = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['availability']
			productInfo = terrafirmaDoc['payload']['products']
			productInfo = productInfo[productInfo.keys()[0]]
			productInfo = Hasher(productInfo)
			primaryProductId = productInfo['primaryProductId']
			wupc = productInfo['wupc']
			usItemId = productInfo['usItemId']
			upc = productInfo['upc']
			productType = productInfo['productType']
			longSku = productInfo['productAttributes']['sku']
			titleVal = productInfo['productAttributes']['productName']
			category = productInfo['productAttributes']['productCategory']['categoryPath']
			information = {"title": titleVal, "price": price, "rollback": rollback, "strikethrough": strikethrough, "reducedPrice": reducedPrice, "clearance": clearance, "store": store, "storeCity": storeCity, "storeName": storeName, "storeAddress": storeAddress, "storeStateOrProvinceCode": storeStateOrProvinceCode, "storePostalCode": storePostalCode, "availability": availability, "quantity": quantity, "primaryProductId": primaryProductId, "wupc": wupc, "usItemId": usItemId, "upc": upc, "productType": productType, "longSku": longSku, "category": category}
			for key, val in information.items():
				if "Hasher" in str(type(information[key])):
					information[key] = ""
			return information
		except Exception as exp:
			if VERBOSE > 5:
				print exp

def local_item_info(store, sku):
	# Returns all store-specific information for a SKU
	header = headers.terrafirm(sku)
	# Generates the header for this request
	params = (('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),)
	# Parameters that specify the data we want to return
	data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(sku, store)
	response = network_request(TERRAFIRM_URL, post=True, headers=header, params=params, data=data)
	# This calls the API endpoint
	if VERBOSE > 3:
		# This will print the api response for debugging
		print response.json()
	return returnPricing(response.json())

def convertSKUToUPC(sku):
	# Converts a walmart SKU number for a UPC
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		res = requests.get('https://brickseek.com/walmart-inventory-checker/?sku={}'.format(sku), headers=headers)
		page = bs4.BeautifulSoup(res.text, 'lxml')
		upc = str(page).partition('upc=')[2].partition('"')[0]
		print("Converted SKU: {} to UPC: {}".format(sku, upc))
		return upc
	except:
		if VERBOSE > 1:
			print("Converting to UPC failed.")
		return None

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores

if __name__ == '__main__':
	VERBOSE = 3
	print local_item_info('2265', 'adsfadsf435188866')
