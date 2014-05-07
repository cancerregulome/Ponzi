#!/usr/bin/env python
"""
ponzi.py
Ryan Bressler, Institute for Systems Biology

Webservice for doing hypergeometric testing against gene sets in a gmt file from the broad:
http://www.broadinstitute.org/gsea/downloads.jsp

Commanly used with kegg pathways:
http://www.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/4.0/c2.cp.kegg.v4.0.symbols.gmt


Start As a tornado webservice Service on port 8000:

ponzi.py 8000 pathwaydb.gmt


See README.md for API.

"""
import json
import numpy as np
import sys
from scipy.stats import hypergeom
import tornado.ioloop
import tornado.web
import tornado.escape
	
def startTornado(port,dbfilename):
	#load needed data into memory
	pathways = []
	defaultbackground = []

	gmtDB = open(dbfilename)
	for line in gmtDB:
		vs=line.rstrip().split("\t")
		setgenes=np.array(vs[2:])
		pathways.append({"name":vs[0],"link":vs[1],"genes":setgenes})
		defaultbackground.extend(setgenes)
	gmtDB.close()

	defaultbackground = np.unique(defaultbackground)

	#this is in here so that the handler is a closure using the
	#local variables holding the pathway and background data
	class MainHandler(tornado.web.RequestHandler):
		def post(self):
			background = defaultbackground
			try:
				args = tornado.escape.json_decode(self.request.body) 
			except ValueError:
				self.clear()
				self.set_status(400)
				self.finish("<html><head><title>400 Bad Request</title></head><body>Malformed JSON object in POST body.</body></html>")
			if "background" in args  and len(args["background"])!=0:
				background = np.unique(args["background"])

			total= len(background)

			replydata = {}
			for setname in args["lists"]:
				genes = np.unique(args["lists"][setname])

				ntrys = len(genes)
	
				names =[]
				links =[]
				probs =[]
				for pathway in pathways:
					setgenes=pathway["genes"]
					nfound = np.sum(np.in1d(genes,setgenes,assume_unique=True))
					if nfound > 1:
						npresent = np.sum(np.in1d(setgenes,background,assume_unique=True))
						prob = hypergeom.sf(nfound-1,total,npresent,ntrys)
						names.append(pathway["name"])
						links.append(pathway["link"])
						probs.append(prob)
				sortedarray = []
				#for i in  np.argsort(np.array(probs))[0:returnn]:
				for i in  np.argsort(np.array(probs)):
					sortedarray.append({"name":names[i],"link":links[i],"p":probs[i]})
				replydata[setname]=sortedarray

			json.dump({'results': replydata}, self)



	application = tornado.web.Application([
		(r"/", MainHandler),
	])
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()

def main():
	if len(sys.argv) == 3:
		startTornado(sys.argv[1],sys.argv[2])
	else:
		print '''Comand line usage:
hypergeom.py genes.txt backgroundgenes.txt pathwaydb.gmt

Start As a tornado webservice Service on port 8000:

hypergeom.py 8000 pathwaydb.gmt'''

if __name__ == '__main__':
	main()
