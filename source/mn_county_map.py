#if running this in Colab make sure the file bdry_counties.gpkg has been uploaded
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px  # Import plotly.express for color scales
import pandas as pd
import os
from datetime import date

# Set the prefix for directory names to be created  
dir_name_prefix = "bee_maps_MN_"
#dir_name_prefix = "county_checker_"
formatted_date = date.today().strftime("%Y%b%d")
dir_name = dir_name_prefix + formatted_date

# Create the directory to store the output files
os.makedirs(dir_name, exist_ok=True)
print(f"Created directory: {dir_name}")

# Read the GeoPackage data
# Assuming your uploaded GeoPackage file is named "bdry_counties.gpkg"
gpkg_path = "bdry_counties.gpkg"
counties_data = gpd.read_file(gpkg_path)
#uncomment to discover what type of data counties_data is
#print("Data type: ",type(counties_data))
# show the columns present in the dataframe
#print("Columns:" ,counties_data.columns)

#add a new empty column to the counties dataframe called 'color'
#update 12/14/24: the new data csv will already have Color1 as first column and Color2 as second column
#counties_data['color'] = ''

#read the BeeOccurence csv into Pandas dataframe
bees = pd.read_csv("MapsData.csv")
#bees = pd.read_csv("BeeCountyOccurrence.csv")
#this is a special test file that has names with exactly 1 county each checked
#bees = pd.read_csv("NewBeeCountyOccurrence_test.csv")
print("first 5 rows of bees",bees.head(5))

#manually set the 3 of columns of data before the county data begins
cols_before_county_data = 3 #primary color, secondary color, scientific name

#perform some data integrity checks...
output_string = ""
output_string += "Counties in GeoPackage: " + str(len(counties_data)) + "\r\n"
output_string += "Number of County columns in Bees data... \r\n"
output_string += "    (total columns less " + str(cols_before_county_data) + " for the scientific name and two colors): " + str(bees.shape[1]-cols_before_county_data) + "\r\n"
output_string += "Number of rows in Bees data: " + str(len(bees)) +"\r\n"


#check that every county in the bees dataframe can be found in the database of counties
#iterate through columns of bees
dataCheckOk = True
for county_column in bees.columns[cols_before_county_data:]:
  #check to see that every column name can be found as a COUNTY_NAM in the geo datafram
  if county_column not in counties_data['COUNTY_NAM'].values:
    output_string +="County name from bees database '" + str(county_column) + "' not found in counties_data. \r\n"
    dataCheckOk = False
if dataCheckOk:
  output_string +="All the counties in bees data are present in geographical data. \r\n"

# do the reciprocal check, make sure every county in the geographical data is in the bees data
#iterate through counties in geodataframe
for county_name in counties_data['COUNTY_NAM']:
  if county_name not in bees.columns:
    output_string +="Bees database place name '" + str(county_name) + "' not found in bees data. \r\n"
    dataCheckOk = False
if dataCheckOk:
  output_string +="All the counties in geographical data are present in bees data. \r\n"

#uncomment to stop here without processing the data
#dataCheckOk = False

print(output_string)

# Save the data inegrity checks string to a text file
file_path = os.path.join(dir_name, "output_stats.txt")
with open(file_path, "w") as f:
    f.write(output_string)


if dataCheckOk:
  #clean up the data in bees by replacing the NaN with letter 'N' for every column
  # Convert specific columns to string before filling missing values
  bees['Scientific Name'] = bees['Scientific Name'].astype(str).fillna('N')
  
  # Replace the 'x' marks with 'C1', this will make the code below easier to read
  # Replace the 'n' marks with 'C2', this will make the code below easier to read
  # do this only for columns 3 to end...skip the first column which is the scientific name
  bees.iloc[:, cols_before_county_data:] = bees.iloc[:, cols_before_county_data:].replace('x', 'C1')
  bees.iloc[:, cols_before_county_data:] = bees.iloc[:, cols_before_county_data:].replace('n', 'C2')

  print("first 5 rows of bees",bees.head(5))

  #loop through all the rows of bees
  # and for each type of bee, map its occurrence in a county to the 'color' field of the counties dataframe
  #for every row of counties_data, use the field COUNTY_NAM to the first row of bees
  #and if the occurrence in that row is Y then set the field 'color' to 'blue'
  #  counties_data.loc[counties_data['COUNTY_NAM'] == row['County'], 'color'] = 'blue'

  border_color = 'black'
  #bee_present_color = '#ADD8E6' #light blue
  #bee_absent_color  = '#FEFEDA' #light yellow

  #bee_present_color = '#FFA500' #orange 
  bee_absent_color  = 'white' 

 
#new way: two colors per bee, color defined by C1 or C2
def populate_occurrences(beesRow, counties_data):
  scientific_name = beesRow['Scientific Name']
  for county in counties_data['COUNTY_NAM']:
    bee_present = beesRow.loc[county] if not pd.isna(beesRow.loc[county]) else 'N'
    
    if bee_present == 'C1':
      color = '#' + beesRow['Color1']
    elif bee_present == 'C2':
      color = '#' + beesRow['Color2']
    else:
      color = bee_absent_color
    counties_data.loc[counties_data['COUNTY_NAM'] == county, 'color'] = color
  return counties_data
  
def plot_geodata(counties_data, plot_title): # New plotting function
  counties_data.plot(facecolor=counties_data['color'], edgecolor=border_color)
  #Heather no longer wants the title on the plot...
  #plt.title(plot_title)
  #limit the amount of whitespace around the plot
  plt.tight_layout()
  #leave off the axes for a cleaner look
  plt.axis("off")
  #use title in filename, but capitalize every word - "Title Case" style
  plot_title = plot_title.title()
  #and then remove spaces
  plot_title = plot_title.replace(" ", "")
  #and also remove any periods from the filename:
  plot_title = plot_title.replace(".", "")

  plt.savefig(os.path.join(dir_name, f"{plot_title}.png"), dpi=600, bbox_inches='tight', pad_inches=0.01)
  
#main processing loop:
for index, row in bees.iterrows():
  updated_counties_data = populate_occurrences(row, counties_data)
  plot_geodata(updated_counties_data, row['Scientific Name'])












