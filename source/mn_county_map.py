import time
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px  # Import plotly.express for color scales
import pandas as pd
import os
from datetime import date
import matplotlib.patches as mpatches

# Start timing
start_time = time.time()

# Set the prefix for directory names to be created  
dir_name_prefix = "bee_maps_MN_"
formatted_date = date.today().strftime("%Y%b%d")
dir_name = dir_name_prefix + formatted_date

# Create the directory to store the output files
os.makedirs(dir_name, exist_ok=True)
print(f"Created directory: {dir_name}")

# Read the GeoPackage data
gpkg_path = "bdry_counties.gpkg"
counties_data = gpd.read_file(gpkg_path)

# Read the BeeOccurrence CSV into Pandas DataFrame
bees = pd.read_csv("MapsData.csv")
print("first 5 rows of bees", bees.head(5))

# Manually set the number of columns of data before the county data begins
cols_before_county_data = 3

# Perform some data integrity checks...
output_string = ""
output_string += "Counties in GeoPackage: " + str(len(counties_data)) + "\r\n"
output_string += "Number of County columns in Bees data... \r\n"
output_string += "    (total columns less " + str(cols_before_county_data) + " for the scientific name and two colors): " + str(bees.shape[1] - cols_before_county_data) + "\r\n"
output_string += "Number of rows in Bees data: " + str(len(bees)) + "\r\n"

# Check that every county in the bees DataFrame can be found in the database of counties
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


# Iterate through columns of bees

bee_absent_color = 'white'
border_color = 'black'  # Define the border color
#clean up the data in bees by replacing the NaN with letter 'N' for every column
# Convert specific columns to string before filling missing values
bees['Scientific Name'] = bees['Scientific Name'].astype(str).fillna('N')
  
# Replace the 'x' marks with 'C1', this will make the code below easier to read
# Replace the 'n' marks with 'C2', this will make the code below easier to read
# do this only for columns 3 to end...skip the first column which is the scientific name
bees.iloc[:, cols_before_county_data:] = bees.iloc[:, cols_before_county_data:].replace('x', 'C1')
bees.iloc[:, cols_before_county_data:] = bees.iloc[:, cols_before_county_data:].replace('n', 'C2')

#print("first 5 rows of bees",bees.head(5))

# New way: two colors per bee, color defined by C1 or C2
def populate_occurrences(beesRow, counties_data):
    scientific_name = beesRow['Scientific Name']
    
    # Create a dictionary to map county names to their bee presence status
    bee_presence_dict = {county: beesRow.loc[county] if not pd.isna(beesRow.loc[county]) else 'N' for county in counties_data['COUNTY_NAM']}
    
    # Create a dictionary to map county names to their colors
    color_dict = {}
    for county, bee_present in bee_presence_dict.items():
        if bee_present == 'C1':
            color_dict[county] = '#' + beesRow['Color1']
        elif bee_present == 'C2':
            color_dict[county] = '#' + beesRow['Color2']
        else:
            color_dict[county] = bee_absent_color
    # Debug print to verify color_dict
    #print("Color Dictionary:", color_dict)   
    # Update the 'color' column in counties_data using the color_dict
    counties_data['color'] = counties_data['COUNTY_NAM'].map(color_dict)
    
    # Debug print to verify updated counties_data
    #print("Updated counties_data with colors:", counties_data[['COUNTY_NAM', 'color']].head())
    
    return counties_data 
   
def plot_geodata(counties_data, plot_title, legend_handles):  # New plotting function
    fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the size as needed
    counties_data.plot(ax=ax, facecolor=counties_data['color'], edgecolor=border_color)
    
    # Limit the amount of whitespace
    plt.tight_layout()
    plt.axis("off")
    
    # Add the legend to the plot
    ax.legend(handles=legend_handles, loc='center right', frameon=False)
    
    # Add title "Minnesota" in the upper right corner with large font
    plt.text(0.80, 0.90, 'Minnesota', fontsize=24, ha='right', va='top', transform=ax.transAxes)
    
    # Use title in filename, but capitalize every word - "Title Case" style
    plot_title = plot_title.title()
    # Remove spaces
    plot_title = plot_title.replace(" ", "")
    # Remove any periods from the filename
    plot_title = plot_title.replace(".", "")
    
    # Save the figure with reduced whitespace and tighter bounding box
    plt.savefig(os.path.join(dir_name, f"{plot_title}.png"), dpi=600, bbox_inches='tight', pad_inches=0.01)
    # plt.savefig("second_sample.png", dpi=300)
    # plt.show()


for index, row in bees.iterrows():
    counties_data = populate_occurrences(row, counties_data)
    
    # Create custom legend handles using the current row of the bees DataFrame
    legend_handles = [
        mpatches.Patch(color='#' + row['Color1'], label='Portman et\nal 2023'),
        mpatches.Patch(color='#' + row['Color2'], label='New record\nsince 2023'),
        mpatches.Patch(color=bee_absent_color, label='Absent')
    ]
    
    plot_geodata(counties_data, row['Scientific Name'], legend_handles)

# End timing
end_time = time.time()

# Calculate and print the total execution time
total_time = end_time - start_time
print(f"Total execution time: {total_time:.2f} seconds")
output_string += f" Total execution time: {total_time:.2f} seconds \r\n"
#output_string +="Bees database place name '" + str(county_name) + "' not found in bees data. \r\n"
    
# Save the data inegrity checks string to a text file
file_path = os.path.join(dir_name, "output_stats.txt")
with open(file_path, "w") as f:
    f.write(output_string)
