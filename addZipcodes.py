import pandas as pd
import sqlite3 as sql
import pandas as pd
from geopy.geocoders import ArcGIS
import time
import shapely.geometry as geom
import geopandas as gpd
from __future__ import division

data = pd.read_csv("police_department_incidents.csv")

# LOAD IN ZIP CODES - from 141B HW 6
zipshapes = gpd.read_file("cb_2015_us_zcta510_500k.shp")

# NARROW IT DOWN SOME
zipshapes = zipshapes[zipshapes.ZCTA5CE10.str.startswith("9")]

# CUT OUT UNNESSESARY STUFF
zipshapes = zipshapes[['geometry', 'ZCTA5CE10']]

points = gpd.GeoDataFrame([geom.asPoint(tuple(row)) for row in data[["X","Y"]].values], columns=["geometry"])
zipcodes = gpd.sjoin(zipshapes, points, how="inner", op="contains") 
data['index_right'] = range(len(data))
newdata = data.merge(zipcodes, on=['index_right'])
newdata['zipcode'] = [str(x) for x in newdata['ZCTA5CE10']]

# DEFINE CODES THAT RESULTED IN SOME KIND OF PUNATIVE ACTION
action = ['ARREST, BOOKED', 'ARREST, CITED', 'JUVENILE BOOKED', 'PROSECUTED BY OUTSIDE AGENCY', 'JUVENILE CITED', 'JUVENILE DIVERTED'
         , 'PROSECTUTED FOR LESSER OFFENSE']

action_taken = [x in action for x in newdata['Resolution']]
newdata['action_taken'] = action_taken

# DROP THE STUFF WE DON'T CARE ABOUT
newdata = newdata.drop('index_right', axis=1)
newdata = newdata.drop('ZCTA5CE10', axis=1)
newdata = newdata.drop('PdId', axis=1)

# Save to csv:
newdata.to_csv("policeWithZip.csv")
print "You can find your csv in the cwd folder with the name policeWithZip.csv"

