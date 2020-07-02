# InvoiceSimilarityCostChecker
Invoice Similarity Cost Checker is a tool that checks the similarity between invoices. It checks the content similarity, layout similarity and merger of both.

## Requirements:
======
```
Conda version: 4.8.3.<br/>
Python version: 3.7.6. <br/>
lxml.etree.ElementTree version: 4.5.1 <br/>
Panda Dataframe version: 1.0.3. <br/>
Matplotlib version: 3.2.1<br/>
Networks version: 2.4<br/>
```

## Tests
======
```
#get 
$ git clone https://github.com/hell03end/pylev3.git
$ cd pylev3
# run
$ python ContentSimilarity.py
$ python LayoutSimilarity.py
$ python mergerMethod.py
```

### - Pre-processing step, transform invoice xml to csv file using InvoiceToCsv.py<br/>
### - Then, choose between the method you want to use to match them(content,structure or content-layout).<br/>


**To get the content similarity between 2 invoices**, use ContentSimilarity.py <br/>
   INPUT: 2 invoices csv files, list of Labels(already defined, see data folder)<br/>
   OUTPUT: similarity value on the content<br/>
   It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
   Those subgraphs are matched between them. 
   At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.

    
**To get the layout similarity between 2 invoices**, use LayoutSimilarity.py<br/>
   INPUT: 2 invoices csv files, list of Labels(already defined, see data folder)<br/>
   OUTPUT: similarity value on the layout<br/>
   It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
   Those subgraphs are transformed to laplacian matrix, then get the similarity between them.
   At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.

**To get the merger of content-layout similarity between 2 invoices**, use mergerMethod.py<br/>
   INPUT: 2 invoices csv files, list of Labels(already defined, see data folder), NormArea.CSV(already defined,see data)<br/>
   OUTPUT: <br/>
   - similarity value on the layout<br/>
   - number of common recognized entities<br/>
   - similarity value on the content<br/>
   It takes 2 invoices in csv file, list of labels,and a list of NormArea.
   An area norm is defined for each entity: it is a surface that each entity would likely appear.
   ISCC checks the contrast of the invoices in two steps: first in the structure.
   If the formats are relatively the same, then in the second step, the contents of each layout are compared.
   It is that average similarity between invoices that is being return.
  

This code is built using:
(https://stackoverflow.com/questions/12122021/python-implementation-of-a-graph-similarity-grading-algorithm)
(https://towardsdatascience.com/using-graph-convolutional-neural-networks-on-structured-documents-for-information-extraction-c1088dcd2b8f)
