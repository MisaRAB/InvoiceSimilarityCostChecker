# InvoiceSimilarityCostChecker
Invoice Similarity Cost Checker is a tool that checks the similarity between invoices. It checks the content similarity, layout similarity and merger of both.

-First step, transform xml to csv file using InvoiceToCsv.py
-Second step, choose between the method you want to use to match them(content,structure or content-layout).

To get the content similarity between 2 invoices, use ContentSimilarity.py
   INPUT: 2 csv files, list of Labels(already defined, see data)
   OUTPUT: similarity value on the content

   It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
   Those subgraphs are matched between them. 
   At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
 '''
 Usage example:
 Uncomment #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
#print(Levenshtein('./data/csv/amazon/amazon0.csv','./data/csv/amazon/amazon0.csv',labels))
 
 run: ContentSimilarity.py
 '''
    
To get the layout similarity between 2 invoices, use LayoutSimilarity.py
   INPUT: 2 csv files, list of Labels(already defined, see data)
   OUTPUT: similarity value on the content

   It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
   Those subgraphs are matched between them.
   At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
 '''
 Usage example:  
 Uncomment #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
#print(Laplacian('./data/csv/amazon/amazon0.csv','./data/csv/amazon/amazon0.csv',labels))
 
 run: LayoutSimilarity.py
 '''  
To get the merger of content-layout similarity between 2 invoices, use mergerMethod.py
   INPUT: 2 csv files, list of Labels(already defined, see data), NormArea.CSV(already defined,see data)
   OUTPUT: -similarity value on the Layout
           -number of recognized entities
           -similarity value on the content

   It takes 2 invoices in csv file, list of labels,and a list of NormArea.
   An area norm is defined for each entity: it is a surface that each entity would likely appear. It is already defined, see data folder.
   ISCC checks the contrast of the invoices in two steps: first in the structure.
   We check if the entity’s location of each invoice is inside the norm area. If yes, then the 0 value is returned as similarity cost.
   If not, the surface outside the norm area is calculated and the cost similarity is computed in function of the norm area
   If the formats are relatively the same, then in the second step, the contents of each layout are compared.
   The words related to each label is picked, transformed into dictionary, then subgraph.
   Those subgraphs are matched between them using Levenshtein algorithm.
   At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
  
   '''
 Usage example:  
 Uncomment #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
 #dataF = pd.read_csv("./data/NormArea.csv")
#print(Laplacian('./data/csv/amazon/amazon0.csv','./data/csv/amazon/amazon0.csv',labels))
 
 run: LayoutSimilarity.py
 '''  
Here is the list of labels:
labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']

This code is built using:
(https://stackoverflow.com/questions/12122021/python-implementation-of-a-graph-similarity-grading-algorithm)
(https://towardsdatascience.com/using-graph-convolutional-neural-networks-on-structured-documents-for-information-extraction-c1088dcd2b8f)
