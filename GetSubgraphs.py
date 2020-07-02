'''
    INPUT: graph, label
    OUTPUT: subgraph corresponding at that label

	It takes a big graph and divide it into subgraphs
'''


import pandas as pd
import numpy as np
import cv2
import os
import collections
import networkx as nx


def getsubgraph(df,wantedLabel):
	'''
	    INPUT: graph, label
	    OUTPUT: subgraph corresponding at that label

		This function takes a big graph and divide it into subgraph and return the subgraph corresponding to the wanted label
	'''
	graph_dict=collections.defaultdict(list)
	df0 = pd.DataFrame(df.loc[df.label == wantedLabel])
	C=0
	for src_id, row in df0.iterrows():
		if row['below_obj_index'] != -1:
			graph_dict[row['Object']] = [row['weight_below']+str(C)]
			graph_dict[row['weight_below']+str(C)] = [row['below_object']]
		if row['side_obj_index'] != -1:
			graph_dict[row['Object']].append(row['weight_right']+str(C))
			graph_dict[row['weight_right']+str(C)] = [row['side_object']]
		C+=1

	return graph_dict
class Graph:
	'''
	    INPUT: dictionary
	    OUTPUT: graph

		This class transform a dictionary into graph.
	'''
	def __init__(self, max_nodes=200):
		self.max_nodes = max_nodes
		return


	def make_graph_data(self, graph_dict):
		'''
			Function that transform a dictionary into graph

			Args:
				G: graph_dict

				{src_id: [dest_id1, dest_id2, ..]}

			Returns:
				G: graph

		'''
		G = nx.from_dict_of_lists(graph_dict)


		return G
