Ponzi
=====

A get enriched quick web service for hypergeometric gene set/pathway over representation analysis.


Data
----
On start up this service will load a gene set database from a [Gene Matrix Transpose (GMT)](http://www.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats#GMT:_Gene_Matrix_Transposed_file_format_.28.2A.gmt.29) file like the ones the broad provides for use with GSEA (licensing restrictions apply to this data):
http://www.broadinstitute.org/gsea/downloads.jsp

It is commonly used with kegg pathways:
http://www.broadinstitute.org/gsea/msigdb/download_file.jsp?filePath=/resources/msigdb/4.0/c2.cp.kegg.v4.0.symbols.gmt

This data will be held in memory for efficient computation.

If you wish to provide your own data, the format is essentially a tsv where each row represents a pathway. The first field is the name of the pathways/geneset, the second is a link or description and the remaining fields contain the gene identifiers:

```
PATHWAY1	http://moreinfo1	gene1	gene2
PATHWAY2	http://moreinfo2	gene2	gene3	gene4
```

Dependencies
------------
This service is written to run as a standalone web server and requires:
* [python2.7](https://www.python.org/)
* [TornadoWeb Webserver](http://www.tornadoweb.org/)
* [NumPy](http://www.numpy.org/)

Usage as a Webservice
---------------------

### Running The Service ###
Start running on port 8000 using pathwaydb.gmt:

```bash
ponzi.py 8000 pathwaydb.gmt
```

### Post gene lists ###
Send a Post Request with json resembling the following in the "genelists" form field:

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

The lists should use the same identifiers as used in gmt. They are considered unordered and repeats elements will be removed before analysis.

If the background genes list is missing or of zero length all genes in the gmt will be used as the background.

### Results ###
The response will contain json containing sorted lists of pathways/genesets like the following:

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
Where p is the probability that there would be at least as much overlap between the lists as was observed and is not corrected for multiple testing.

Testing and Benchmarking
------------------------

The script testquery.py can be used to benchmark and test the service by querying for each of pathways in the source gmt. It will report the time elapsed for each query, the total time and the number of correctly identified pathways. The service should correctly identify all KEGG pathways in about .04 seconds per (single list) request round trip.

```
$ testquery.py http://localhost:8000 c2.cp.kegg.v4.0.symbols.gmt 
Request for KEGG_GLYCOLYSIS_GLUCONEOGENESIS took  0.0512459278107
Request for KEGG_CITRATE_CYCLE_TCA_CYCLE took  0.0337159633636
...
Request for KEGG_PRIMARY_IMMUNODEFICIENCY took  0.0303318500519
Request for KEGG_HYPERTROPHIC_CARDIOMYOPATHY_HCM took  0.0496649742126
Request for KEGG_ARRHYTHMOGENIC_RIGHT_VENTRICULAR_CARDIOMYOPATHY_ARVC took  0.0445010662079
Request for KEGG_DILATED_CARDIOMYOPATHY took  0.0574429035187
Request for KEGG_VIRAL_MYOCARDITIS took  0.0639088153839
186  requests took  8.37595295906 . 0.0450320051562  per request.
Correctly identified  186  /  186 pathways.
```


