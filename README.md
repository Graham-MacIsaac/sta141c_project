# sta141c_project

Here is information on how to run all of our files. Watch out for the libraries each file uses, espeically if running this code on the server. 

# addZipcodes.py

|    |    |  
|----|----|  
Run: 						| `python addZipcodes.py`
Does: 						| Adds zipcodes to the original data
Returns: 					| `policeWithZip.csv`
Have in the same folder: 	| `police_department_incidents.csv` (From [SFOpenData](https://data.sfgov.org/Public-Safety/Police-Department-Incidents/tmnf-yvry)) and 								cb_2015_us_zcta510_500k.shp ([From here](https://www.census.gov/geo/maps-data/data/cbf/cbf_zcta.html))
							 
# stringsToNum.py

|    |    |  
|----|----|  
Run:						| `python stringsToNum.py`
Does:						| Adds four extra columns to the data with a number mapping for each string predictor we are using
Returns: 					| `policeZipNum.csv`	
Have in the same folder:	| `policeWithZip.csv`

# categoryToNum.txt   
Contains the information for what numbers were mapped to each category. 

# districtToNum.txt  
Contains the information for what numbers were mapped to each police district. 

# SVM10.py
|    |    |  
|----|----|  
Run:						| `python SVM10.py`
Does:						| Prints the accuracy of predicting action_taken from category, pddistrict, and zipcode using support vector machine for 10% of the data
Have in the same folder:	| `policeZipNum.csv`

# logistic_regression.R  

|    |    |  
|----|----|  
| Run:						| `Rscript logistic_regression.R` |  
| Does:						| Prints the model and trainaing accuracy of logistic regression to predict if an action was taken for an incident |  
| Have in the same folder:		| `policeZipNum.csv` |  


