import pandas as pd
import numpy as np
import cv2
import os
import collections
import networkx as nx


class caseBox:
	'''
		Description:
		-----------
			This class is used to check the contrast of the invoices in two steps: first in the structure.
            We check if the entity’s location of each invoice is inside the norm area. If yes, then the 0 value is returned as similarity cost.
            If not, the surface outside the norm area is calculated and the cost similarity is computed in function of the norm area
            An area norm is defined for each entity: it is a surface that each entity would likely appear.


	'''

	def __init__(self, label_column='label'):
		self.label_column = label_column
		self.df = None
		self.count = 0

	def read(self, object_map):

		'''
			Function to ensure the data is in correct format

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


	def Box(self,labels):
		'''
			Function to find the entities in a invoice

			Args:
				labels: list of labels possible in a invoice(already defined)

			Return:
				dataframe with all the geographical localization of each entity

		'''
		df = self.df

		# check if object map was successfully read by .read() method
		try:
			if len(df) == 0:
				return
		except:
			return

		# initialize empty df to store plotting coordinates
		dfX = pd.DataFrame(columns=['Label','xmin', 'xmax', 'ymin', 'ymax'])
		# ================== Box======================================== #
		Xmax=0;Ymax=0; Xmin=10000;Ymin=10000
		PXmax=0;PYmax=0; PXmin=10000;PYmin=10000
		KPXmax=0;KPYmax=0; KPXmin=0;KPYmin=0
		for label in labels:
			df0 = pd.DataFrame(df.loc[df.label == label])
			if len(df0)!=0: #if the label exist, get all the entities coordinaties
				for src_idx, row in df0.iterrows():
					if(PXmin==10000): #if its the first time
						PXmin=int(row['xmin'])
						PYmin=int(row['ymin'])
						PXmax=int(row['xmax'])
						PYmax=int(row['ymax'])
					if(abs(int(row['xmin'])-PXmin)<1000 and abs(int(row['ymin'])-PYmin)<1000): 		# if two entity are too big from each other even tho with the same label, consider them separate
						Xmin=min(int(row['xmin']),Xmin)
						Ymin=min(int(row['ymin']),Ymin)
						Xmax=max(int(row['xmax']),Xmax)
						Ymax=max(int(row['ymax']),Ymax)
					else:
						Xmin=int(row['xmin'])
						Ymin=int(row['ymin'])
						Xmax=int(row['xmax'])
						Ymax=int(row['ymax'])
						KPXmin=PXmin
						KPYmin=PYmin
						KPXmax=PXmax
						KPYmax=PYmax

					PXmin=Xmin
					PYmin=Ymin
					PXmax=Xmax
					PYmax=Ymax

				# put all the coordonate in the dataframe
				data={'Label':label,'xmin':Xmin, 'xmax':Xmax, 'ymin':Ymin, 'ymax':Ymax}
				dfX=dfX.append(data,ignore_index=True)
				if (KPXmin!=0):
					data0={'Label':label,'xmin':KPXmin, 'xmax':KPXmax, 'ymin':KPYmin, 'ymax':KPYmax}
					dfX=dfX.append(data0,ignore_index=True)
				Xmax=0;Ymax=0; Xmin=10000;Ymin=10000
				PXmax=0;PYmax=0; PXmin=10000;PYmin=10000
				KPXmax=0;KPYmax=0; KPXmin=0;KPYmin=0


		return dfX

def IsDfInDataF(NormArea, DF, labels):
	'''
	INPUT: NormArea(already defined), DF as the invoice list of entities coordinates in dataframe, labels(already defined),
	NormArea: it is a surface that each entity would likely appear.
	OUTPUT: layout similarity cost of each label in dataframe

	This function check if the region of an entity is within the AreaNorm and deliver the distance with is how far/close it is.
	'''
	dfreturn = pd.DataFrame(columns=['Label','Distvalue'])

    #go to each label and compare each to the norm area of that label
	for label in labels:
		pdNorm=pd.DataFrame(NormArea.loc[NormArea.Label == label]).values.tolist()
		pd0=pd.DataFrame(DF.loc[DF.Label == label]).values.tolist()
		if len(pdNorm)!=0 and len(pd0)!=0:
			for i0 in range(len(pd0)):
				s=pd0[i0]
				Min=1000
				for i1 in range(len(pdNorm)):
					t=pdNorm[i1]
					Min=min(checkGeography(t,s)*100, Min)
				#put the label and the value distance in a dataframe for later use
				data0={'Label':label,'Distvalue':Min}
				dfreturn=dfreturn.append(data0,ignore_index=True)

	return dfreturn

def checkGeography(norm, square):
	'''
	INPUT: NormArea for a label, localization of an entity in an invoice for a label.
	NormArea: it is a surface that each entity would likely appear. It is already defined in NormArea.csv
	OUTPUT: distance from the NormArea.

	This function checks if the entity’s location of each invoice is inside the norm area. If yes, then the 0 value is returned as similarity cost.
	If not, the surface outside the norm area is calculated and the cost similarity is computed in function of the norm area
	'''
	surfaceNorm=(norm[2]-norm[1])*(norm[4]-norm[3])
	XminS=square[1]
	YminS=square[3]
	XmaxS=square[2]
	YmaxS=square[4]
	XminN=norm[1]
	YminN=norm[3]
	XmaxN=norm[2]
	YmaxN=norm[4]
	if XminS>=XminN and YminS>=YminN and XmaxS<=XmaxN and YmaxS<=YmaxN:
		return 0
	elif XminS<XminN and YminS<YminN:
		#print('Case 1')
		return (abs(YminS-YminN)*abs(XminS-XminN))/ surfaceNorm
	elif XminS>=XminN and YminS<YminN and XmaxS<=XmaxN:
		#print('Case 2')
		return (abs(YminS-YminN)*abs(XminS-XmaxS))/ surfaceNorm
	elif YminS<YminN and XmaxS>XmaxN :
		#print('Case 3')
		return (abs(YminS-YminN)*abs(XmaxS-XmaxN))/ surfaceNorm
	elif XminS<XminN and YminS>=YminN and YmaxS<=YmaxN:
		#print('Case 4')
		return (abs(YminS-YmaxS)*abs(XminS-XminN))/ surfaceNorm
	elif  YminS>=YminN and XmaxS>XmaxN and YmaxS<=YmaxN:
		#print('Case 6')
		return (abs(YminS-YmaxS)*abs(XmaxS-XmaxN))/ surfaceNorm
	elif XminS<XminN and YmaxS>YmaxN:
		#print('Case 7')
		return (abs(YmaxS-YmaxN)*abs(XminS-XminN))/ surfaceNorm
	elif XminS>=XminN and XmaxS<=XmaxN and YmaxS>YmaxN:
		#print('Case 8')
		return (abs(YmaxS-YmaxN)*abs(XminS-XmaxS))/ surfaceNorm
	elif XmaxS>XmaxN and YmaxS>YmaxN:
		#print('Case 9')
		return (abs(YmaxS-YmaxN)*abs(XmaxS-XmaxN))/ surfaceNorm
	else:
		print('ERROR')
		return -1
