Ponzi
=====

A get (en)rich(ed) quick service.


(Proposed) Usage as A Webservice
----------------------

Start running on port 8000 useing pathwaydb.gmt:

```bash
hypergeom.py 8000 pathwaydb.gmt
```

Send a Post Request with the following in the genelists field:

```json
{
"lists":{
	"list1": [
	          "gene1", 
	          "gene2"
	         ],
	"list2": [
	          "gene1", 
	          "gene2", 
	          "gene3"
	         ]
	},
"background": [
               "gene1", 
               "gene2", 
               "gene3", 
               "gene4"
              ]
}
```

Use the same gene identifiers as in the gmt.
If background is missing or of zero length all genes in the gmt will be used as the background.

Recieve a sorted list of pathways/genesets like the following:

```json
{
"results": {
	"list1": [
		   { 
			"name": "PATHWAY1",
			"link": "http://moreinfo1",
			"p": 0.1
		   },
		   {
			"name": "PATHWAY2",
			"link": "http://moreinfo2",
			"p": 0.2
		   },
			...
		],
	"list2": [
		  ...
		],
	...
	}
}
```

