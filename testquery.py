#!/usr/bin/env python
"""
Test and benchmakr tornado webservice Service on port 8000:

hypergeom.py http://localhose:8000 pathwaydb.gmt
"""
import sys
import urllib
import urllib2
import json
import time

def main():
	url = sys.argv[1]
	gmtDB = open(sys.argv[2])

	
	totalstart = time.time()
	requests = 0
	corect = 0
	for line in gmtDB:
		vs=line.rstrip().split("\t")
		setgenes=vs[2:]
		requestdata=urllib.urlencode({"genelists":json.dumps({"lists":{"list1":setgenes}})})
		start = time.time()
		result = urllib2.urlopen(url,requestdata)

		print "Request for", vs[0],"took ",  time.time()-start #, " got :\n", result.read()
		requests += 1
		if vs[0]==json.load(result)["list1"][0]["name"]:
			corect +=1
		
	totaltime = time.time() - totalstart

	print requests,  " requests took ", totaltime, ". ", totaltime/requests, " per request." 
	print "Correctly identified ", corect, " / ", requests, "pathways."

if __name__ == '__main__':
	main()