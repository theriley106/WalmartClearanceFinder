import argparse

THREADS = 30
ALL_SKUS = "MasterList.txt"
# Default thread count



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-o','--output', help='Specify csv output', required=False, default=None)
	parser.add_argument('-t','--threads', help='Specify thread count', required=False, default=THREADS)
	parser.add_argument('-s','--store', help='Specify store to search', required=True)
	parser.add_argument('-i','--input', help='Specify SKU list or single sku', required=False, default=ALL_SKUS)
	args = vars(parser.parse_args())
	# Contains a dictionary of all arguments
	if '.' not in args['input']:
		# This means it's a single sku search
		skuList = [args['input']]
		# Creates a list with a single item
	else:
		# This means it's a file input
		skuList = [x for x in open(args['input']).read().split("\n") if len(x) > 0]
		# Creates a list from the file input
	print skuList
