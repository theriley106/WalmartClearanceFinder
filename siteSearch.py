import walmart

#walmart.search_walmart("iphone", "2265")


#print len(walmart.get_all_facets("https://www.walmart.com/search/api/preso?query=a&cat_id=0&stores=1123&prg=mWeb"))


searchTerm = raw_input("Search Term: ")
for val in walmart.gen_search_urls(searchTerm, "2265"):
	print val
