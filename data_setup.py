#!/usr/bin/env python

"""
Usage: python2 data_setup.py Police_Department_Incidents.csv cb_2015_us_zcta510_500k.shp
"""

from __future__ import division
import pandas as pd
from geopy.geocoders import ArcGIS
import time
import shapely.geometry as geom
import geopandas as gpd
import sys






def main():
    # If a crime data path and zip data path were given as arguments
    if len(sys.argv) == 3:
        crime_data_path = sys.argv[1]
        zip_data_path = sys.argv[2]
    else:
        try:
            crime_data_path = "C:\Users\Graham\Documents\STA 141C\project\police_department_incidents.csv"
            zip_data_path = "C:\Users\Graham\Documents\STA 141C\project\cb_2015_us_zcta510_500k/cb_2015_us_zcta510_500k.shp"
        except:
            print("Usage: python2 data_setup.py Police_Department_Incidents.csv cb_2015_us_zcta510_500k.shp")

    data = pd.read_csv(crime_data_path)

    # LOAD IN ZIP CODES
    zipshapes = gpd.read_file(zip_data_path)

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


    # Export the prepared data frame for use in other scripts
    newdata.to_hdf('crime.h5','table',append=False)


if __name__ == '__main__':
    main()