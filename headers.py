import json
HEADERS = json.load(open("headers.json"))

def terrafirm(sku):
	# Headers for terrafirm request
	# Requires item SKU

	header = HEADERS['terrafirm']
	header['referer'] = "https://www.walmart.com/product/{}/sellers".format(sku)
	return header
