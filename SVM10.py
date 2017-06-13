#!/usr/bin/env python2

import pandas as pd
from sklearn import svm
import time

def main():
	"""
	This script runs SVM for 10% of the data.
	Running it on the whole data set would take over a day.
	"""
	start = time.clock()
	
	# Read in the data:
	crime = pd.read_csv("policeZipNum.csv")
	
	# Drop any variable we are not using for prediction:
	crime = crime.drop(['Unnamed: 0', "geometry", 'IncidntNum', "Descript", "DayOfWeek", "Date", "Time", "Resolution", "Address", "X", "Y", "Location"], axis=1)
	crime = crime.drop(['Unnamed: 0.1', "Category", "PdDistrict", "action_taken"], axis = 1)
		
	# Get 10 percent of the data randomly:
	crime = crime.sample(frac = 0.10)
	
	# Get testing and training:
	train = crime.sample(frac = 0.8)
	test = crime.drop(train.index)
	
	# Split into x and y and convert to matrix:
	xtrain = train.drop("action_takenNum", axis = 1).as_matrix()
	xtest = test.drop("action_takenNum", axis = 1).as_matrix()
	ytrain = train["action_takenNum"].as_matrix()
	ytest = test["action_takenNum"].as_matrix()
	
	# Run SVM:
	clf = svm.SVC()
	clf.fit(xtrain, ytrain) 
	preds = clf.predict(xtest)
	
	# Get accuracy:
	acc = float(sum(preds == ytest)) / ytest.shape[0]
	
	# Print results:
	print "SVM gave an accuracy of ", acc
	
	print "Total time: ", time.clock() - start
	
if __name__ == "__main__": main()
