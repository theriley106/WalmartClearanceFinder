# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import argparse
import helper
import threading
import csv
import time
import random
from time import gmtime, strftime

lock = threading.Lock()

THREADS = 30
CSV_UPDATE_INTERVAL = 30
# This is the frequency of CSV Updates
ALL_SKUS = "data/MasterList.txt"
# Default thread count
SEARCH_VALS = []
ALL_ITEMS = []
CSV_HEADERS = ["skuVal", "title", "price", "quantity", "store", "availability", "primaryProductId", "category", "longSku", "rollback", "productType", "storeName", "storeAddress", "storeCity", "strikethrough", "upc", "usItemId", "storePostalCode", "storeStateOrProvinceCode", "reducedPrice", "clearance", "wupc"]
COMPLETED = []
STATIC_VALS = []

def get_current_time():
	return strftime("%Y-%m-%d-%H-%M-%S", gmtime())

CSV_FILE = "{}.csv".format(get_current_time())

def update_csv(fileName):
	with open(fileName, "wb") as f:
		toWrite = [CSV_HEADERS] + ALL_ITEMS
		writer = csv.writer(f)
		writer.writerows(toWrite)

def search():
	while len(SEARCH_VALS) > 0:
		try:
			lock.acquire()
			searchVal = SEARCH_VALS.pop(0)
			lock.release()
			skuNumber = searchVal['sku']
			storeNumber = searchVal['store']
			val = helper.local_item_info(storeNumber, skuNumber)
			#print val
			#print val.keys()
			if val != None:
				if val['availability'] == "NOT_AVAILABLE" and STATIC_VALS[1] == True:
					pass
				else:
					val['skuVal'] = skuNumber
					if helper.VERBOSE > 1:
						print "{} | {} | {} | {} | {}/{}\n".format(val['title'][:40], val['price'], skuNumber, len(ALL_ITEMS), len(COMPLETED), STATIC_VALS[0]),
					tVal = []
					for key in CSV_HEADERS:
						tVal.append(val[key])
					ALL_ITEMS.append(tVal)
		except Exception as exp:
			if helper.VERBOSE > 3:
				print("ERROR: {}".format(exp))
			try:
				lock.release()
			except:
				pass
		try:
			COMPLETED.append(searchVal)
		except:
			pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-o','--output', help='Specify csv output', required=False, default=CSV_FILE)
	parser.add_argument('-t','--threads', help='Specify thread count', required=False, default=THREADS)
	parser.add_argument('-s','--store', help='Specify store to search', required=False, default=None)
	parser.add_argument('-i','--input', help='Specify SKU list or single sku', required=False, default=ALL_SKUS)
	parser.add_argument('-v','--verbose', help='Verbose Mode', required=False, default=False)
	parser.add_argument('-a','--allstock', help='Show all items regardless of availability', required=False, default="False")
	args = vars(parser.parse_args())
	# Contains a dictionary of all arguments
	if args['verbose'] != False:
		# Sets verbose setting
		try:
			helper.VERBOSE = int(args['verbose'])
		except:
			helper.VERBOSE = 5
	if '.' not in args['input']:
		# This means it's a single sku search
		skuList = [args['input']]
		# Creates a list with a single item
	else:
		# This means it's a file input
		skuList = [x for x in open(args['input']).read().split("\n") if len(x) > 0]
		# Creates a list from the file input
	if args['store'] == None:
		# This means the user did not specify a store number
		storeVals = helper.GrabAllStoreNumbers()
		# Creates a list of every store
	else:
		# The user specified a single store
		storeVals = [args['store']]
		# Creates a list with a single item
	totalVals = 0
	for store in storeVals:
		# Iterates through all inputted stores
		for sku in skuList:
			# Iterates through all inputted skus
			SEARCH_VALS.append({"sku": sku, "store": store})
			totalVals += 1
			# Creates a list of all search terms
	random.shuffle(SEARCH_VALS)
	STATIC_VALS.append(totalVals)
	STATIC_VALS.append((args['allstock'] != "False"))
	thread_count = args['threads']
	threads = [threading.Thread(target=search) for _ in range(thread_count)]
	for thread in threads:
		thread.daemon = True
		thread.start()
	while len(COMPLETED) != totalVals:
		# This allows you to kill the thread
		try:
			time.sleep(5)
			try:
				lock.acquire()
				# Gets lock to wait on active processes
				update_csv(args['output'])
				lock.release()
			except Exception as exp:
				print("CSV ERROR: {}".format(exp))
				try:
					lock.relase()
				except:
					pass
		except:
			print("Program Killed...")
			lock.acquire()
			# Gets lock to wait on active processes
			update_csv(args['output'])
			lock.release()
			raise Exception("Program Killed...")
