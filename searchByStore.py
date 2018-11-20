import argparse
import walmart
import threading
import csv
import time

lock = threading.Lock()

THREADS = 30
ALL_SKUS = "MasterList.txt"
# Default thread count
SEARCH_VALS = []
ALL_ITEMS = []

def search():
	while len(SEARCH_VALS) > 0:
		try:
			lock.acquire()
			searchVal = SEARCH_VALS.pop(0)
			lock.release()
			skuNumber = searchVal['sku']
			storeNumber = searchVal['store']
			val = walmart.local_item_info(storeNumber, skuNumber)
			print "{}\n".format(val),
			# Threading safe printing
			if val != None and val['Quantity'] != 'Out of stock' and val['isVal'] == True:
				ALL_ITEMS.append(val)
				print("{} | {} | {} | {} | {}/{}".format(x['title'][:40], val['Price'], sku, len(ALL_ITEMS), START_LEN-len(SKUS), START_LEN))
		except Exception as exp:
			if walmart.VERBOSE > 3:
				print("ERROR: {}".format(exp))
			try:
				lock.release()
			except:
				pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-o','--output', help='Specify csv output', required=False, default=None)
	parser.add_argument('-t','--threads', help='Specify thread count', required=False, default=THREADS)
	parser.add_argument('-s','--store', help='Specify store to search', required=False, default=None)
	parser.add_argument('-i','--input', help='Specify SKU list or single sku', required=False, default=ALL_SKUS)
	parser.add_argument('-v','--verbose', help='Verbose Mode', required=False, default=False)
	args = vars(parser.parse_args())
	# Contains a dictionary of all arguments
	if args['verbose'] != False:
		# Sets verbose setting
		try:
			walmart.VERBOSE = int(args['verbose'])
		except:
			walmart.VERBOSE = 5
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
		storeVals = walmart.GrabAllStoreNumbers()
		# Creates a list of every store
	else:
		# The user specified a single store
		storeVals = [args['store']]
		# Creates a list with a single item
	for store in storeVals:
		# Iterates through all inputted stores
		for sku in skuList:
			# Iterates through all inputted skus
			SEARCH_VALS.append({"sku": sku, "store": store})
			# Creates a list of all search terms
	thread_count = args['threads']
	threads = [threading.Thread(target=search) for _ in range(thread_count)]
	for thread in threads:
		thread.daemon = True
		thread.start()
	while True:
		# This allows you to kill the thread
		try:
			time.sleep(1)
		except:
			with lock:
				# Gets lock to wait on active processes
				raise Exception("Program Killed...")

