import pandas as pd
import sqlite3 as sql
import pandas as pd
from geopy.geocoders import ArcGIS
import time
import shapely.geometry as geom
import geopandas as gpd
from __future__ import division

data = pd.read_csv("C:\Users\Graham\Documents\STA 141C\project\police_department_incidents.csv")

# LOAD IN ZIP CODES
zipshapes = gpd.read_file("C:\Users\Graham\Documents\STA 141C\project\cb_2015_us_zcta510_500k/cb_2015_us_zcta510_500k.shp")

# NARROW IT DOWN SOME
zipshapes = zipshapes[zipshapes.ZCTA5CE10.str.startswith("9")]

#CUT OUT UNNESSESARY STUFF
zipshapes = zipshapes[['geometry', 'ZCTA5CE10']]

points = gpd.GeoDataFrame([geom.asPoint(tuple(row)) for row in data[["X","Y"]].values], columns=["geometry"])
zipcodes = gpd.sjoin(zipshapes, points, how="inner", op="contains")
data['index_right'] = range(len(data))
newdata = data.merge(zipcodes, on=['index_right'])
newdata['zipcode'] = [str(x) for x in newdata['ZCTA5CE10']]

#DEFINE CODES THAT RESULTED IN SOME KIND OF PUNATIVE ACTION
action = ['ARREST, BOOKED', 'ARREST, CITED', 'JUVENILE BOOKED', 'PROSECUTED BY OUTSIDE AGENCY', 'JUVENILE CITED', 'JUVENILE DIVERTED'
         , 'PROSECTUTED FOR LESSER OFFENSE']

action_taken = [x in action for x in newdata['Resolution']]
newdata['action_taken'] = action_taken

#DROP THE STUFF WE DON'T CARE ABOUT
newdata = newdata.drop('index_right', axis=1)
newdata = newdata.drop('ZCTA5CE10', axis=1)
newdata = newdata.drop('PdId', axis=1)

####################
## BEGIN-ANALYSIS ##
####################

# Newdata is the original dataframe with zipcodes attached. note that the same crime will be listed multiple times if it falls under several different categories

#67% OF ALL ARRESTS END IN NO ACTION
overall_action_rate = [sum(newdata['action_taken']==False)/len(newdata)

#GET COUNTS PER CRIME CATEGORY
counts = [len(newdata[newdata['Category']==x]) for x in list(set(newdata['Category']))]
categories = list(set(newdata['Category']))
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
db = sql.connect('C:\Users\Graham\Documents\STA 141C\project\sf_data.sqlite')
cursor = db.execute("SELECT * FROM sqlite_master")
zillow = pd.read_sql("SELECT * from zillow", db)

