import pandas as pd
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss
import time

data = pd.read_csv('policeZipNum.csv')

def main():
    
    n = len(data)
    else:
        X = np.array(data[['PdDistrictNum', 'CategoryNumber', 'zipcode']])
        y = np.array(data[['action_takenNum']])

    X_train, y_train = X[:round(n*0.6)], y[:round(n*0.6)]
    X_valid, y_valid = X[round(n*0.6):round(n*0.8)], y[round(n*0.6):round(n*0.8)]
    X_train_valid, y_train_valid = X[:round(n*0.8)], y[:round(n*0.8)]
    X_test, y_test = X[round(n*0.8):], y[round(n*0.8):]

    # Train uncalibrated random forest classifier on whole train and validation
    # data and evaluate on test data
    clf = RandomForestClassifier(n_estimators=15)
    clf.fit(X_train_valid, y_train_valid)
    clf_probs = clf.predict_proba(X_test)
    score = log_loss(y_test, clf_probs)

    pred = clf.predict(X_test)
    print 'The accuracy of the random forest is:', sum(sum(pred==y_test.T))/float(len(X_test))
    print 'log-loss = ', score
    print "Total time: ", time.clock() - start

if __name__ == "__main__": main()
