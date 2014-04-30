'''
File: feature_vector.py
--------------------------------------------------------------------
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

This file implements SVM method.

Author: Bowei Zhang and Jingxin Zhu
Date created: 29th, Apr
--------------------------------------------------------------------
'''

class Feature_Vector:
	def process(self, row = None):
		try:
			dim = 22
			vec = [False] * dim

			vec[0] = int(row[0])
			vec[1] = row[1]
			vec[2] = int(row[2])
			vec[3] = self.label(row[3])
			vec[4] = int(row[4])
			vec[5] = int(row[5])
			vec[6] = row[6]
			vec[7] = self.label(row[7])
			vec[8] = self.label(row[8])
			vec[9] = int(row[9])
			vec[10] = int(row[10])
			vec[11] = self.label(row[11])
			vec[12] = self.label(row[12])
			vec[13] = self.label(row[13])
			vec[14] = self.label(row[14])
			vec[15] = self.label(row[15])
			vec[16] = self.label(row[16])
			vec[17] = self.label(row[17])
			vec[18] = int(row[18])
			vec[19] = int(row[19])
			vec[20] = int(row[20])
			vec[21] = int(row[21])
			return vec
		except:
			print 'Unexpected format of input file'
			return []

	def label(self, flag):
		if (flag == 'True'):
			return 1
		else:
			return 0
