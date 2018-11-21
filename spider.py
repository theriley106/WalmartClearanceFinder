# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import re
import bs4
import threading
import time
import json
THREAD_COUNT = 30
ALL_ITEMS = []
TO_SEARCH = ["46708712"]
VISITED = []
lock = threading.Lock()
def extract_item_nums(string):
	return set(re.findall("athcpid\S(\d+)", string))

#"https://quimby.mobile.walmart.com/tempo?tenant=Walmart.com&channel=WWW&pageType=ItemPage&enrich=athenaunified,iro&item=SKUVALUE&p13n={%22pageId%22:%22SKUVALUE%22,%22catId%22:%220:1105910:1127173:1231261%22,%22itemInfo%22:{%22itemAvailabilityStatus%22:%22IN_STOCK%22,%22itemOfferType%22:%22ONLINE_AND_STORE%22,%22isPrimaryOfferPUTEligible%22:true,%22walledGarden%22:%22false%22},%22userReqInfo%22:{%22referer%22:null},%22userClientInfo%22:{%22deviceType%22:%22desktop%22,%22callType%22:%22CLIENT%22}}".replace("SKUVALUE", sku)
def get_info():
	while True:
		while len(TO_SEARCH) == 0:
			time.sleep(1)
		lock.acquire()
		sku = TO_SEARCH.pop()
		lock.release()
		pull_page(sku)

def save_info():
	while True:
		time.sleep(60)
		with open('data.json', 'w') as outfile:
			json.dump(ALL_ITEMS, outfile)


def pull_page(sku):
	url = "https://quimby.mobile.walmart.com/tempo?tenant=Walmart.com&channel=WWW&pageType=ItemPage&enrich=athenaunified,iro&item=SKUVALUE&p13n={%22pageId%22:%22SKUVALUE%22,%22catId%22:%220:1105910:1127173:1231261%22,%22itemInfo%22:{%22itemAvailabilityStatus%22:%22IN_STOCK%22,%22itemOfferType%22:%22ONLINE_AND_STORE%22,%22isPrimaryOfferPUTEligible%22:true,%22walledGarden%22:%22false%22},%22userReqInfo%22:{%22referer%22:null},%22userClientInfo%22:{%22deviceType%22:%22desktop%22,%22callType%22:%22CLIENT%22}}".replace("SKUVALUE", sku)
	res = requests.get(url)
	modules = res.json()['modules']
	for a in modules:
		itemCategories = a['configs'].keys()
		for key in itemCategories:
			try:
				for val in a["configs"][key]["products"]:
					sku = val['id']['usItemId']
					raw_input(val)
					titleVal = val["productName"]
					if sku not in VISITED:
						lock.acquire()
						VISITED.append(sku)
						ALL_ITEMS.append({"sku": sku, "title": titleVal})
						print("{} | {} | {}".format(sku, len(ALL_ITEMS), titleVal))
						TO_SEARCH.append(sku)
						lock.release()
			except Exception as exp:
				print exp
				pass

if __name__ == '__main__':
	get_info()
	raw_input("Continue: ")
	#sku = "719650769"
	#url = "https://www.walmart.com/ip/{}".format(sku)
	#res = requests.get(url)
	#page = bs4.BeautifulSoup(res.text, 'lxml')
	#for link in page.find_all('a', href=True):
	#	print link['href']
	#print "athcpid" in str(page)
	threads = [threading.Thread(target=get_info) for i in range(THREAD_COUNT)]
	for thread in threads:
		thread.start()
	t = threading.Thread(target=save_info)
	t.start()
	for threading in threads:
		thread.join()
	t.join()
