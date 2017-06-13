import pandas as pd
import random
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss

data = pd.read_csv('policeZipNum.csv')

def randomForest(n=None):
    if n is None:
        n = len(data)
    #MUST BE MULTIPLE OF 10
    
    if n == len(data):
        sampind = random.sample(range(1, 2063699), n)
        X = np.array(data[['PdDistrictNum', 'CategoryNumber', 'zipcode']].loc[sampind])
        y = np.array(data[['action_takenNum']].loc[sampind])
    else:
        X = np.array(data[['PdDistrictNum', 'CategoryNumber', 'zipcode']])
        y = np.array(data[['action_takenNum']])

    X_train, y_train = X[:n*0.6], y[:n*0.6]
    X_valid, y_valid = X[n*0.6:n*0.8], y[n*0.6:n*0.8]
    X_train_valid, y_train_valid = X[:n*0.8], y[:n*0.8]
    X_test, y_test = X[n*0.8:], y[n*0.8:]

    # Train uncalibrated random forest classifier on whole train and validation
    # data and evaluate on test data
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train_valid, y_train_valid)
    clf_probs = clf.predict_proba(X_test)
    score = log_loss(y_test, clf_probs)

    pred = clf.predict(X_test)
    print 'The accuracy of the random forest is:', sum(sum(pred==y_test.T))/float(len(X_test))


