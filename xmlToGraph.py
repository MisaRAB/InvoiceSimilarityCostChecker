import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import cv2
import os
from PIL import Image
import collections
from matplotlib import pyplot as plt
import networkx as nx
import time
def xmlToObject(xmlPath):
    '''
    INPUT: xml
    OUTPUT: dataframe
    this function treats the xml file into an arranged dataframe with 5 columns:xmin, xmax, ymin, ymax, Object, label
    '''
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    words=[]
    Xmin=[]
    Ymin=[]
    Xmax=[]
    Ymax=[]
    tag=[]

    for item in root.findall(".//DL_ZONE"):
            words.append(item.get('contents'))
            xmin=item.get('col')
            Xmin.append(xmin)
            Xmax.append(int(xmin)+int(item.get('width')))
            ymin=item.get('row')
            Ymin.append(ymin)
            Ymax.append(int(ymin)+int(item.get('height')))
            tag.append(item.get('correctclass'))

    d={'xmin': Xmin, 'xmax': Xmax, 'ymin': Ymin, 'ymax': Ymax, 'Object': words, 'label': tag}
    df = pd.DataFrame(data=d)
    return df

def ObjectList(df,nearest_idx):
    '''
    INPUT: list of index
    OUTPUT: list of words related to each index
    '''
    list=[]
    for index in nearest_idx:
            s=df.loc[df.index==index, 'Object'].values
            list.append(", ".join(s))
    return list


class ObjectTree:
	'''
		Description:
		-----------
			This class is used to generate a dictionary of list that contain
			the graph structure:
				{src_id: [dest_id1, dest_id2, ..]}
			and return the list of text entities in the input document

		Example use:
		-----------
			>> connector = ObjectTree(label_column='label')
			>> connector.read(object_map_df, img)
			>> df, obj_list = connector.connect(plot=False, export_df=False)
	'''

	def __init__(self, label_column='label'):
		self.label_column = label_column
		self.df = None
		self.count = 0


	def read(self, object_map):

		'''
			Function to ensure the data is in correct format and saves the
			dataframe and image as class properties

			Args:
				object_map: pd.DataFrame, having coordinates of bounding boxes,
										  text object and label

			Returns:
				None

		'''

		assert type(object_map) == pd.DataFrame,f'object_map should be of type \
			{pd.DataFrame}. Received {type(object_map)}'


		assert 'xmin' in object_map.columns, '"xmin" not in object map'
		assert 'xmax' in object_map.columns, '"xmax" not in object map'
		assert 'ymin' in object_map.columns, '"ymin" not in object map'
		assert 'ymax' in object_map.columns, '"ymax" not in object map'
		assert 'Object' in object_map.columns, '"Object" column not in object map'
		assert self.label_column in object_map.columns, \
						f'"{self.label_column}" does not exist in the object map'



		# drop unneeded columns
		required_cols = {'xmin', 'xmax', 'ymin', 'ymax', 'Object',
							self.label_column}
		un_required_cols = set(object_map.columns) - required_cols
		object_map.drop(columns=un_required_cols, inplace=True)
		self.df = object_map
		return



	def connect(self):
		'''
			This method implements the logic to generate a graph based on
			visibility. If a horizontal/vertical line can be drawn from one
			node to another, the two nodes are connected.

			Args:
				none
		'''
		df = self.df

		# check if object map was successfully read by .read() method
		try:
			if len(df) == 0:
				return
		except:
			return


		# initialize empty lists to store coordinates and distances
		# ================== vertical======================================== #
		distances, nearest_dest_ids_vert = [], []

		x_src_coords_vert, y_src_coords_vert, x_dest_coords_vert, \
		y_dest_coords_vert = [], [], [], []

		# ======================= horizontal ================================ #
		lengths, nearest_dest_ids_hori = [], []

		x_src_coords_hori, y_src_coords_hori, x_dest_coords_hori, \
		y_dest_coords_hori = [], [], [], []
		# ================== weight======================================== #
		weight_below, weight_right = [], []

		for src_idx, src_row in df.iterrows():

			# ================= vertical ======================= #
			src_range_x = (src_row['xmin'], src_row['xmax'])
			src_center_y = (int(src_row['ymin']) + int(src_row['ymax']))/2

			dest_attr_vert = []

			# ================= horizontal ===================== #
			src_range_y = (src_row['ymin'], src_row['ymax'])
			src_center_x = (int(src_row['xmin']) + int(src_row['xmax']))/2

			dest_attr_hori = []


			################ iterate over destination objects #################
			for dest_idx, dest_row in df.iterrows():
				dest_range_x= (dest_row['xmin'], dest_row['xmax'])
				dest_center_y = (int(dest_row['ymin']) + int(dest_row['ymax']))/2

				height = dest_center_y - src_center_y
				dest_range_y = (dest_row['ymin'], dest_row['ymax'])
				# flag to signal whether the destination object is below source
				is_beneath = False
				if not src_idx == dest_idx:
					# ==================== vertical ==========================#

					# consider only the cases where destination object lies
					# below source
					if dest_center_y > src_center_y and \
                    dest_range_y[1] in range(int(src_range_y[1]), int(src_range_y[1])+200 ) and \
					dest_range_x[1] in range(int(src_range_x[1])-100, int(src_range_x[1])+100 ):
						# check if horizontal range of dest lies within range
						# of source

						# case 1
						if dest_range_x[0] <= src_range_x[0] and \
							dest_range_x[1] >= src_range_x[1]:

							x_common = (int(src_range_x[0]) + int(src_range_x[1]))/2
							line_src = (x_common , src_center_y)
							line_dest = (x_common, dest_center_y)

							attributes = (dest_idx, line_src, line_dest, height)
							dest_attr_vert.append(attributes)

							is_beneath = True

						# case 2
						elif dest_range_x[0] >= src_range_x[0] and \
							dest_range_x[1] <= src_range_x[1]:

							x_common = (int(dest_range_x[0]) + int(dest_range_x[1]))/2
							line_src = (x_common, src_center_y)
							line_dest = (x_common, dest_center_y)

							attributes = (dest_idx, line_src, line_dest, height)
							dest_attr_vert.append(attributes)

							is_beneath = True

						# case 3
						elif dest_range_x[0] <= src_range_x[0] and \
							dest_range_x[1] >= int(src_range_x[0]) and \
								dest_range_x[1] < int(src_range_x[1]):

							x_common = (int(src_range_x[0]) + int(dest_range_x[1]))/2
							line_src = (x_common , src_center_y)
							line_dest = (x_common, dest_center_y)

							attributes = (dest_idx, line_src, line_dest, height)
							dest_attr_vert.append(attributes)

							is_beneath = True

						# case 4
						elif int(dest_range_x[0]) <= int(src_range_x[1]) and \
							dest_range_x[1] >= int(src_range_x[1]) and \
								dest_range_x[0] > src_range_x[0]:

							x_common = (int(dest_range_x[0]) + int(src_range_x[1]))/2
							line_src = (x_common , src_center_y)
							line_dest = (x_common, dest_center_y)

							attributes = (dest_idx, line_src, line_dest, height)
							dest_attr_vert.append(attributes)

							is_beneath = True

				if not is_beneath:
					# ======================= horizontal ==================== #
						#dest_range_y = (dest_row['ymin'], dest_row['ymax'])
						# get center of destination NOTE: not used
						dest_center_x = (int(dest_row['xmin']) + int(dest_row['xmax']))/2

						# get length from destination center to source center
						if dest_center_x > src_center_x:
							length = dest_center_x - src_center_x
						else:
							length = 0

						# consider only the cases where the destination object
						# lies to the right of source

						if dest_center_x > src_center_x and \
						dest_center_y==src_center_y and dest_center_x-src_center_x<=300:
							#check if vertical range of dest lies within range
							# of source
							# case 1
							if dest_range_y[0] >= src_range_y[0] and \
								dest_range_y[1] <= src_range_y[1]:

								y_common = (int(dest_range_y[0]) + int(dest_range_y[1]))/2
								line_src = (src_center_x, y_common)
								line_dest = (dest_center_x, y_common)

								attributes = (dest_idx, line_src, line_dest, length)
								dest_attr_hori.append(attributes)

							# case 2
							if dest_range_y[0] <= src_range_y[0] and \
								dest_range_y[1] <= src_range_y[1] and \
									dest_range_y[1] > int(src_range_y[0]):

								y_common = (int(src_range_y[0]) + int(dest_range_y[1]))/2
								line_src = (src_center_x, y_common)
								line_dest = (dest_center_x, y_common)

								attributes = (dest_idx, line_src, line_dest, length)
								dest_attr_hori.append(attributes)

							# case 3
							if dest_range_y[0] >= src_range_y[0] and \
								dest_range_y[1] >= src_range_y[1] and \
									int(dest_range_y[0]) < src_range_y[1]:

								y_common = (int(dest_range_y[0]) + int(src_range_y[1]))/2
								line_src = (src_center_x, y_common)
								line_dest = (dest_center_x, y_common)

								attributes = (dest_idx, line_src, line_dest, length)
								dest_attr_hori.append(attributes)

							# case 4
							if dest_range_y[0] <= src_range_y[0] \
								and dest_range_y[1] >= src_range_y[1]:

								y_common = (int(src_range_y[0]) + int(src_range_y[1]))/2
								line_src = (src_center_x, y_common)
								line_dest = (dest_center_x, y_common)

								attributes = (dest_idx, line_src, line_dest, length)
								dest_attr_hori.append(attributes)

			# sort list of destination attributes by height/length at position
			# 3 in tuple
			dest_attr_vert_sorted = sorted(dest_attr_vert, key = lambda x: x[3])
			dest_attr_hori_sorted = sorted(dest_attr_hori, key = lambda x: x[3])

			# append the index and source and destination coords to draw line
			# ==================== vertical ================================= #
			if len(dest_attr_vert_sorted) == 0:
				nearest_dest_ids_vert.append(-1)
				x_src_coords_vert.append(-1)
				y_src_coords_vert.append(-1)
				x_dest_coords_vert.append(-1)
				y_dest_coords_vert.append(-1)
				distances.append(0)
			else:
				nearest_dest_ids_vert.append(dest_attr_vert_sorted[0][0])
				x_src_coords_vert.append(dest_attr_vert_sorted[0][1][0])
				y_src_coords_vert.append(dest_attr_vert_sorted[0][1][1])
				x_dest_coords_vert.append(dest_attr_vert_sorted[0][2][0])
				y_dest_coords_vert.append(dest_attr_vert_sorted[0][2][1])
				distances.append(dest_attr_vert_sorted[0][3])

			# ========================== horizontal ========================= #
			if len(dest_attr_hori_sorted) == 0:
				nearest_dest_ids_hori.append(-1)
				x_src_coords_hori.append(-1)
				y_src_coords_hori.append(-1)
				x_dest_coords_hori.append(-1)
				y_dest_coords_hori.append(-1)
				lengths.append(0)

			else:
			# try and except for the cases where there are vertical connections
			# still to be made but all horizontal connections are accounted for
				try:
					nearest_dest_ids_hori.append(dest_attr_hori_sorted[0][0])
				except:
					nearest_dest_ids_hori.append(-1)

				try:
					x_src_coords_hori.append(dest_attr_hori_sorted[0][1][0])
				except:
					x_src_coords_hori.append(-1)

				try:
					y_src_coords_hori.append(dest_attr_hori_sorted[0][1][1])
				except:
					y_src_coords_hori.append(-1)

				try:
					x_dest_coords_hori.append(dest_attr_hori_sorted[0][2][0])
				except:
					x_dest_coords_hori.append(-1)

				try:
					y_dest_coords_hori.append(dest_attr_hori_sorted[0][2][1])
				except:
					y_dest_coords_hori.append(-1)

				try:
					lengths.append(dest_attr_hori_sorted[0][3])
				except:
					lengths.append(0)
		#=========use for relative distance: NEAR-MEDIUM-FAR into the vertical and horizontal=========#

		for d,l in zip(distances,lengths):

			if d!=0 and d<40:
				weight_below.append('NV') #Near-Medium-Far
			elif(d>=40 and d<=90):
				weight_below.append('MV')
			elif(d>90):
				weight_below.append('FV')
			else:
				weight_below.append(' ')
			if l!=0 and l<50:
				weight_right.append('NH')
			elif(l>=50 and l<=150):
				weight_right.append('MH')
			elif(l>150):
				weight_right.append('FH')
			else:
				weight_right.append(' ')


		# ==================== vertical ===================================== #
		# create df for plotting lines
        #rows: nearest_dest_ids_vert, column:'Object',  the .values attribute to return the values as a np array

		df['below_object'] = pd.Series(ObjectList(self.df, nearest_dest_ids_vert))

		# add distances column
		df['below_dist'] = distances

		# add column containing index of destination object
		df['below_obj_index'] = nearest_dest_ids_vert


		# ==================== horizontal =================================== #
		# create df for plotting lines
		df['side_object'] = pd.Series(ObjectList(self.df, nearest_dest_ids_hori))

		# add lengths column
		df['side_length'] = lengths

		# add column containing index of destination object
		df['side_obj_index'] = nearest_dest_ids_hori
		# ======================== weight =============================== #

		df['weight_below'] = weight_below
		df['weight_right'] = weight_right

		return df
