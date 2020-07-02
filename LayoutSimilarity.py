'''
    INPUT: 2 invoices csv files, list of Labels
    OUTPUT: similarity value on the layout

    It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are transformed to laplacian matrix, then get the similarity between them.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']

    Usage example:
    Uncomment: #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
    #print(Laplacian('./data/amazon0.csv','./data/amazon1.csv',labels))
    Run: LayoutSimilarity.py
'''
from GetSubgraphs import *


def Laplacian(CSVPath1,CSVPath2,labels):
    '''
    It take 2 invoices in csv file and list of labels. The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are matched between them.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    '''
    count=0
    Lap=0
    graph0=Graph()
    graph1=Graph()
    dfX0= pd.read_csv(CSVPath1)
    dfX1= pd.read_csv(CSVPath2)
    for label in labels:
        graph_dict0= getsubgraph(dfX0,label)
        graph_dict1= getsubgraph(dfX1,label)

        G0 = graph0.make_graph_data(graph_dict0)
        G1 = graph1.make_graph_data(graph_dict1)
        if(len(graph_dict0)!=0 and len(graph_dict1)!=0):
            count+=1
            Lap+=eigenSimilarity(G0,G1)

    return Lap/count

def select_k(spectrum, minimum_energy = 0.9):
    '''
    select 90% of the eigenvalues of each graph
    '''
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)

def eigenSimilarity(graph1,graph2):
    '''
    transform each graph to laplacian matrix, select 90% of the eigenvalues of each graph, then get the similarity between them.
    '''
    laplacian1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacian2 = nx.spectrum.laplacian_spectrum(graph2)

    k1 = select_k(laplacian1)
    k2 = select_k(laplacian2)
    k = min(k1, k2)

    return ( sum((laplacian1[:k] - laplacian2[:k])**2))

labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
print(Laplacian('./data/amazon0.csv','./data/amazon1.csv',labels))
