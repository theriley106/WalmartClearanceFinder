# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Set default encoding to UTF-8

import os
import requests
import random
import threading
import json
import csv
import sys
import bs4
import time
import subprocess
import re
lock = threading.Lock()
STARTTIME = time.time()
TIMEOUT = 10
Proxies = [{}]
THREADS = 20
PRIMARYDICT = []
SKUS = json.load(open("data.json"))
ALL_ITEMS = []
START_LEN = len(SKUS)

def GrabAllStoreNumbers():
	ListOfStores = []
	with open('Walmarts.csv', 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	for line in your_list:
		if 'Walmart Supercenter' in str(line[1]):
			ListOfStores.append(line[0])
	return ListOfStores

def GrabElement(json, element):
	json = json.partition(str(element) + '":')[2]
	json = json.partition(',')[0]
	if '"' in str(json):
		json = json.replace('"', '')
	if '{' in str(json):
		json = json.replace('{', '')
	if '}' in str(json):
		json = json.replace('}', '')
	return json


def SearchStore(store, SKU):
	a = {}
	a['Store'] = str(store)
	data = {
			'authority': 'www.walmart.com',
			'method': 'POST',
			'path': '/store/ajax/search',
			'scheme': 'https',
			'accept' : 'application/json, text/javascript, */*; q=0.01',
			'accept-encoding' : 'gzip, deflate, br',
			'accept-language' : 'en-US,en;q=0.8',
			'content-length' : '55',
			'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin' : 'https://www.walmart.com',
			'referer' : 'https://www.walmart.com/store/{}/search?query={}'.format(store, SKU),
			'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest',
			"searchQuery":"store={}&query={}".format(store, SKU),


			}

	url = "https://www.walmart.com/store/ajax/search"
	res = requests.post(url, data=data, proxies=random.choice(Proxies))
	res = res.json()
	print res
	try:
		a["Price"] = int((GrabElement(str(res), 'priceInCents')))
	except:
		pass

	a["Quantity"] = (GrabElement(str(res), 'quantity'))
	return a




def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def searchSKU(storeList, UPC):
	for store in storeList:
		if (time.time() - STARTTIME) < (60*TIMEOUT):
			try:
				suggestions_list = random.choice(listOfStores)
				newData = searchStoreByUPC(store, UPC)
				if newData != None:
					newData["Price"]
					lock.acquire()
					print {"Store": store, "Price": newData["Price"], "Quantity": newData["Quantity"]}
					PRIMARYDICT.append({"UPC": UPC, "Store": store, "Price": int(newData["Price"]), "Quantity": newData["Quantity"]})
					lock.release()
			except Exception as exp:
				pass
		else:
			return

def saveToCSV(listVar, UPC):
	with open("{}.csv".format(UPC), "w") as fp:
		wr = csv.writer(fp, dialect='excel')
		list1 = ["Store", "Price", "Quantity"]
		wr.writerow(list1)
		wr.writerow([""])
		for listItem in listVar:
			list1 = [listItem["Store"], '${:,.2f}'.format(int(listItem["Price"] * .01)), listItem["Quantity"]]
			wr.writerow(list1)

def do_all():
	while len(SKUS) > 0:
		try:
			lock.acquire()
			x = SKUS.pop(0)
			lock.release()
			sku = x['sku']
			val = grabTerraFirma('2265', sku)
			if val != None and val['Quantity'] != 'Out of stock' and val['isVal'] == True:
				ALL_ITEMS.append(val)
				print("{} | {} | {} | {} | {}/{}".format(x['title'][:40], val['Price'], sku, len(ALL_ITEMS), START_LEN-len(SKUS), START_LEN))
		except Exception as exp:
			try:
				lock.release()
			except:
				pass
			pass


if __name__ == '__main__':
	#raw_input(grabTerraFirma('631', '779112907'))
	#returnPricing(val)
	threads = [threading.Thread(target=do_all) for i in range(THREADS)]
	for thread in threads:
		thread.start()
	for threading in threads:
		thread.join()
