import pandas as pd


def main():
	"""
	Adds on columns for category, pddistrict, and action_taken that replace the strings with numbers 
	Takes a few minutes to run
	"""
	
	# Read in the data:
	crime = pd.read_csv("policeWithZip.csv")
	
	# CATEGORY
	# ========
	
	# Get a mapping for each category -> number
	categoryToNum = dict()
	i = 0
	for crimeType in crime["Category"].unique():
		categoryToNum[crimeType] = i
		i += 1 
		
	# Add new column with the number values:
	catNums = [categoryToNum[row["Category"]] for index, row in crime.iterrows()]
	crime["CategoryNumber"] = catNums
	
	# Save dictionary to text file to reference later:
	f = open("categoryToNum.txt","w")
	f.write( str(categoryToNum) )
	f.close()
	
	# PDDISTRICT
	# =========
	
	# Get a mapping for each district -> number
	districtToNum = dict()
	i = 0
	for district in crime["PdDistrict"].unique():
		districtToNum[district] = i
		i += 1 
		
	# Add new column with the number values:
	distNums = [districtToNum[row["PdDistrict"]] for index, row in crime.iterrows()]
	crime["PdDistrictNum"] = distNums
	
	# Save dictionary to text file to reference later:
	f = open("districtToNum.txt","w")
	f.write( str(districtToNum) )
	f.close()
	
	# ACTION_TAKEN
	# ============
	
	actionToNum = {False : 0, True: 1}

	# Add new column with the number values:
	actionNums = [actionToNum[row["action_taken"]] for index, row in crime.iterrows()]
	crime["action_takenNum"] = actionNums
	
	# Save dictionary to text file to reference later:
	f = open("actionToNum.txt","w")
	f.write( str(actionToNum) )
	f.close()
	
	
	# Save the updated csv:
	crime.to_csv("policeZipNum.csv")

if __name__ == "__main__": main()

