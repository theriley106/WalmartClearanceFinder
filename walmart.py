import requests
import json
import headers
VERBOSE = False
REQUEST_TIMEOUT = 10
NETWORK_RETRY = 3

def network_request(url, headers, params=None, timeout=None, network_retry=None):
	# This is the function that makes network requests
	if network_retry == None:
		# Sets params to default
		network_retry = NETWORK_RETRY
	if timeout == None:
		# Sets params to default
		timeout = REQUEST_TIMEOUT
	for _ in range(network_retry):
		res = requests.get(url, headers=headers, param=params, timeout=timeout)
		# Makes the network request
		if res.status_code == 200:
			# This means it was successful
			return res


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
	header = headers.terrafirm(sku)
	# Generates the header for this request
	params = (
	    ('rgs', 'OFFER_PRODUCT,OFFER_INVENTORY,OFFER_PRICE,VARIANT_SUMMARY'),
	)
	# Parameters that specify the data we want to return
	data = '{{"itemId":"{}","paginationContext":{{"selected":false}},"storeFrontIds":[{{"usStoreId":{},"preferred":false,"semStore":false}}]}}'.format(sku, store)
	response = requests.post('https://www.walmart.com/terra-firma/fetch', headers=header, params=params, data=data, timeout=10)
	print response.status_code
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
