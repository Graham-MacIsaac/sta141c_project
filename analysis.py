#!/usr/bin/env python

"""
Usage: python2 analysis.py sf_data.sqlite
"""

from __future__ import division
import pandas as pd
import sqlite3 as sql
#from geopy.geocoders import ArcGIS
import time
#import shapely.geometry as geom
#import geopandas as gpd
import sys


def main():
    
    # If a crime data path and zip data path were given as arguments
    if len(sys.argv) == 2:
        sf_db_path = sys.argv[1]
    else:
        try:
            sf_db_path = 'C:\Users\Graham\Documents\STA 141C\project\sf_data.sqlite'
        except:
            print("Usage: python2 analysis.py sf_data.sqlite")



    # Import h5 created in data_setup.py
    crime_hdf = pd.HDFStore('crime.h5')
    newdata = crime_hdf.select('/table')
    print(newdata.head())

    
    ####################
    ## BEGIN-ANALYSIS ##
    ####################

    # Newdata is the original dataframe with zipcodes attached. note that the same crime will be listed multiple times if it falls under several different categories

    #67% OF ALL ARRESTS END IN NO ACTION
    overall_action_rate = [sum(newdata['action_taken']==False)/len(newdata)]

    #GET COUNTS PER CRIME CATEGORY
    categories = list(set(newdata['Category'])) #???
    counts = [len(newdata[newdata['Category']==x]) for x in categories]
    category_counts = pd.DataFrame([counts, categories]).T

    action = [(sum(newdata[newdata['zipcode']==x]['action_taken']==True)/len(newdata[newdata['zipcode']==x]))
    for x in list(set(newdata['zipcode']))]
    zips = list(set(newdata['zipcode']))

    #RATE OF POLICE ACTIONS TAKEN ACCROSS ALL CRIMES BY ZIPCODE
    action_rate_zips = pd.DataFrame([action, zips]).T
    action_rate_zips.columns = ['action_taken', 'zips']

    #ACTION RATE BY CRIME TYPE ACCROSS ALL ZIPCODES
    action = [(sum(newdata[newdata['Category']==x]['action_taken']==True)/len(newdata[newdata['Category']==x]))
    for x in list(set(newdata['Category']))]
    action_rate_category = pd.DataFrame([action, categories]).T
    action_rate_category.columns = ['action_taken', 'categories']
    action_rate_category.sort_values(by='action_taken')

    #GET ACTION RATE BY CRIME FOR EACH INDIVIDUAL ZIPCODE
    #a = [pd.DataFrame([x, categories]) for x in oh_lawrdy]
    #crime_info = [x.transpose() for x in a]

    #for i in range(len(crime_info)):
    #    crime_info[i].columns = ['action_rate', 'category']


    #SAMPLE SIZES FOR THE FOLLOWING CATEGORIES ARE TOO SMALL TO BE USEFUL
    ['SEX OFFENCES, NON FORCIBLE', 'TREA', 'PORNOGRAPHY/OBSCENE MAT', 'GAMBLING']

    #MAYBE WORK IN ZILLOW DATA SOMEHOW?
    db = sql.connect(sf_db_path)
    cursor = db.execute("SELECT * FROM sqlite_master")
    zillow = pd.read_sql("SELECT * from zillow", db)



if __name__ == '__main__':
    main()