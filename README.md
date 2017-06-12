# sta141c_project

Here is information on how to run all of our files. Watch out for the libraries each file uses, espeically if running this code on the server. 

# addZipcodes.py
	
	Run: 						python addZipcodes.py 
	Does: 						Adds zipcodes to the original data
	Returns: 					policeWithZip.csv
	Have in the same folder: 	police_department_incidents.csv (From SFOpenData: https://data.sfgov.org/Public-Safety/Police-Department-Incidents/tmnf-yvry)
								cb_2015_us_zcta510_500k.shp (From here: https://www.census.gov/geo/maps-data/data/cbf/cbf_zcta.html)
							 
# stringsToNum.py

	Run:						python stringsToNum.py
	Does:						Adds three extra columns to the data with a number matching for each string predictor we are using
	Returns: 					policeZipNum.csv
	Have in the same folder:	policeWithZip.csv

# categoryToNum.txt -> contains the information for what numbers were mapped to each category. 

# districtToNum.txt -> contains the information for what numbers were mapped to each police district. 

# SVM.py
	Run:						python SVM.py
	Does:						Prints the accuracy of predicting action_taken from category, pddistrict, and zipcode using support vector machine
	Have in the same folder:	policeZipNum.csv
