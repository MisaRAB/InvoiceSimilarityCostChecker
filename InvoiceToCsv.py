'''
    INPUT:  invoice xml
    OUTPUT: invoice saved into csv

    This is a pre-processing step. The invoice is transformed in dataframe with all the connection on the right and left of each words.

    usage example: storeDf('./data/xml/amazon/0.xml')
'''
from xmlToGraph import *


#save a xml into csv with all the neighbor from the right and beneath
def storeDf(xml1Path,wantedName):
    df0 = xmlToObject(xml1Path)
    tree0 = ObjectTree()
    tree0.read(df0)
    dfX0= tree0.connect() #"NOtImportant" parameter is not important but needed to make function work
    CSV_PATH = './data/'+wantedName+'.csv'
    dfX0.to_csv(CSV_PATH, index = None)
    return dfX0

storeDf('./data/amazon0.xml','amazon0')
