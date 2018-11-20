import requests
import json
VERBOSE = False

def returnPricing(terrafirmaDoc):
	# Extracts pricing information from the terrafirm API response
	for key, value in terrafirmaDoc['payload']['offers'].items():
		try:
			price = terrafirmaDoc['payload']['offers'][key]['pricesInfo']['priceMap']['CURRENT']['price']
			store = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]['storeId']
			quantity = terrafirmaDoc['payload']['offers'][key]['fulfillment']['pickupOptions'][0]["inStoreStockStatus"]
			return {"Store": store, "Price": price, "Quantity":quantity}
		except Exception as exp:
			if VERBOSE:
				print exp
			pass

def local_item_info(store, sku):
	# Returns all store-specific information for a SKU
	headers = {
	    'pragma': 'no-cache',
	    'content-type': 'application/json',
	    'accept': '*/*',
	    'cache-control': 'no-cache',
	    'authority': 'www.walmart.com',
	    'referer': 'https://www.walmart.com/product/{}/sellers'.format(sku),
		}

	params = (
	    ('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),
	)

	data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(sku, store)

	response = requests.post('https://www.walmart.com/terra-firma/fetch', headers=headers, params=params, data=data, timeout=10)
	if VERBOSE:
		print json.dumps(response.json())
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
		if VERBOSE:
			print("Converting to UPC failed.")
		return None

if __name__ == '__main__':
	print local_item_info('2265', '779112907')
