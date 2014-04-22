Ponzi
=====

A get (en)rich(ed) quick web service for hypergeometric gene set analysis.


Data
----
On start up this service will load a gene set database from a [Gene Matrix Transpose (GMT)](http://www.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats#GMT:_Gene_Matrix_Transposed_file_format_.28.2A.gmt.29) file like the ones the broad provides for use with GSEA (licensing restrictions apply to this data):
http://www.broadinstitute.org/gsea/downloads.jsp

It is commanly used with kegg pathways:
http://www.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/4.0/c2.cp.kegg.v4.0.symbols.gmt

This data will be held in memory for effichent computation.

If you wish to provide your own data the format is essentially a tsv where each row represents a pathway. The first field is the name of the pathways/geneset, the second is a link or description and the remaining fields contain the gene identifiers

```
PATHWAY1	http://moreinfo1	gene1	gene2
PATHWAY2	http://moreinfo2	gene2	gene3	gene4
```

Dependencies
------------
This service requires:
* [python2.7](https://www.python.org/)
* [TornadoWeb](http://www.tornadoweb.org/)
* [Numpy](http://www.numpy.org/)

Ussage as Webservice
--------------------

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

