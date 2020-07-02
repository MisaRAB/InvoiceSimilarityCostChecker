'''
    INPUT: 2 invoices csv files, list of Labels(already defined, see data folder), NormArea.CSV(already defined,see data folder)
    OUTPUT: -similarity value on the Layout
            -number of recognized entity
            -similarity value on the content

    It takes 2 invoices in csv file, list of labels and a list of NormArea.
    ISCC checks the contrast of the invoices in two steps: first in the structure.
    We check if the entity’s location of each invoice is inside the norm area. If yes, then the 0 value is returned as similarity cost.
    If not, the surface outside the norm area is calculated and the cost similarity is computed in function of the norm area
    An area norm is defined for each entity: it is a surface that each entity would likely appear. If the formats are relatively the same, then in the second step, the contents of each layout are compared.
    The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are matched between them using Levenshtein algorithm.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']

    Usage example:
    Uncomment #labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IN','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
    #NormArea = pd.read_csv("./data/NormArea.csv")
    #print(Compare2Layout('./data/amazon0.csv', './data/amazon1.csv',labels,NormArea))
    Run: mergerMethod.py
'''

from GetSubgraphs import *
from graph_edit_distance import *
from Layout import *

def Compare2Layout(CSVPath1,CSVPath2,labels,dataF):
    '''
    INPUT: 2 csv files, list of Labels(already defined, see data folder), NormArea.CSV(already defined, see data folder)
    OUTPUT: -similarity value on the Layout
            -number of recognized entity
            -similarity value on the content

    This function calculate the layout similarity.  If the formats are relatively the same, then in the second step, the contents of each layout are compared.
    '''
    df2= pd.read_csv(CSVPath1)
    df3= pd.read_csv(CSVPath2)
    box2 = caseBox()
    box3 = caseBox()
    box2.read(df2)
    box3.read(df3)
    dfX2=box2.Box(labels)
    #print('==================')
    dfX3=box3.Box(labels)

    RecognizedLabel=[]
    lab0=[]
    dfLayout0=IsDfInDataF(dataF,dfX2,labels)
    dfLayout1=IsDfInDataF(dataF,dfX3,labels)
    ContentSIMIValue=0
    LayoutCost=0
    MINCost=1000
    for label in labels:
        #take each label and compare the  value of cost between 2 invoices
        df00 = pd.DataFrame(dfLayout0.loc[dfLayout0.Label == label]).values.tolist()
        df11 = pd.DataFrame(dfLayout1.loc[dfLayout1.Label == label]).values.tolist()
        #if the label exista in both
        if len(df00)!=0 and len(df11)!=0:
            lab0.append(label)
            #if the label exista in both
            if (len(df00)==len(df11)):
                #if the label have the same number of appearance  and if they are less 10% far from each other, do the ContentSimilarity
                for i in range(len(df00)):
                    if abs(df00[i][1]-df11[i][1])<10:
                        RecognizedLabel.append(label)
                        LayoutCost+=  abs(df00[i][1]-df11[i][1])
                        ContentSIMIValue+=contentSimilarity(CSVPath1,CSVPath2,label)

            elif (len(df00)!=len(df11)):
                #if the label have the different number of appearance, take the minimum cost between them. if they are less 10% far from each other, do the ContentSimilarity
                if (len(df00)>len(df11)):
                    maxL=len(df00)
                    minL=len(df11)
                    dfmax=df00
                    dfmin=df11
                else:
                    maxL=len(df11)
                    minL=len(df00)
                    dfmax=df11
                    dfmin=df00
                for i in range(minL):
                    for j in range(maxL):
                        if abs(dfmax[j][1]-dfmin[i][1])<10:
                            MINCost=min(abs(dfmax[j][1]-dfmin[i][1]),MINCost)
                if (MINCost<10):
                    RecognizedLabel.append(label)
                    LayoutCost+= MINCost
                    ContentSIMIValue+=contentSimilarity(CSVPath1,CSVPath2,label)
        MINCost=1000

    return LayoutCost/len(RecognizedLabel),RecognizedLabel, ContentSIMIValue/len(RecognizedLabel)

def EGD(graph1,graph2):
    '''
    INPUT: 2 graphs
    OUTPUT: Content similarity value

    This function calculate the least transformation from graph1 to graph2 using Levenshtein algorithm.
    '''
    ged = GraphEditDistance(graph1,graph2)
    dist=ged.normalized_distance()
    #print(dist)
    return(dist)

def contentSimilarity(CSVPath1,CSVPath2,label):
    '''
    INPUT: 2 invoices csv type, list of labels
    OUTPUT: Content similarity value

    The words related to each label is picked, transformed into dictionary, then subgraph.
    Those subgraphs are matched between them using Levenshtein algorithm.
    At the end, we add the similarity value of each label and compute the average. It is that average similarity that is being return.
    '''
    lab=[]
    result=0
    result1=0
    graph0=Graph()
    graph1=Graph()
    dfX0= pd.read_csv(CSVPath1)
    dfX1= pd.read_csv(CSVPath2)
    graph_dict0= getsubgraph(dfX0,label)
    graph_dict1= getsubgraph(dfX1,label)
    G0 = graph0.make_graph_data(graph_dict0)
    G1 = graph1.make_graph_data(graph_dict1)
    return EGD(G0,G1)





labels=['SN','SA','SCN','SCID','SCPOR','SFAX','SVAT','BN','BA','SHN', 'SHA', 'SHSA', 'UP', 'PTWTX', 'TXR', 'TWTX', 'TA', 'TTX','IDATE', 'ONUM', 'PMODE', 'SSIRET', 'STOA','CNUM']
NormArea = pd.read_csv("./data/NormArea.csv")
print(Compare2Layout('./data/amazon0.csv', './data/amazon0.csv',labels,NormArea)) #amazon
