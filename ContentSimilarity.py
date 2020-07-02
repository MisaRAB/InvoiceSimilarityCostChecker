'''
    INPUT: 2 invoices csv files, list of Labels(already defined)
    OUTPUT: similarity value on the content

    It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are matched between them using Levenshtein algorithm.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']

    Usage example:
    Uncomment: #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
    #print(Levenshtein('./data/amazon0.csv','./data/amazon1.csv',labels))
    Run: ContentSimilarity.py

'''
from GetSubgraphs import *
from graph_edit_distance import *

def Levenshtein(CSVPath1,CSVPath2,labels):
    '''
    It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are matched between them using Levenshtein algorithm.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    '''
    Lev=0
    graph0=Graph()
    graph1=Graph()
    dfX0= pd.read_csv(CSVPath1)
    dfX1= pd.read_csv(CSVPath2)
    for label in labels:
        graph_dict0= getsubgraph(dfX0,label) #X and Y are not important parameter but needed to make function work
        graph_dict1= getsubgraph(dfX1,label)

        G0 = graph0.make_graph_data(graph_dict0)
        G1 = graph1.make_graph_data(graph_dict1)
        Lev+=EGD(G0,G1)

    return Lev/len(labels)


def EGD(graph1,graph2):
    '''
    calculate the least transformation from graph1 to graph2
    '''
    ged = GraphEditDistance(graph1,graph2)
    dist=ged.normalized_distance()
    return(dist)

labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
print(Levenshtein('./data/amazon0.csv','./data/amazon1.csv',labels))
