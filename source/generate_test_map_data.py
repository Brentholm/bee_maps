#chatGPT wrote this code. It uses the header line from the file that Heather gave me, and uses it 
#to generate a csv file that will have each county checked once
#the purpose is to create a series of 87 maps, such that the one called "Aitkin_test" will have Aitkin county highlighted
#and so on through all the counties.

import pandas as pd

# Load the CSV file
file_path = 'BeeCountyOccurrence_short.csv'
df = pd.read_csv(file_path)

# Get the list of counties from the header (excluding the 'Scientific Name' column)
counties = df.columns[1:]

# Create a new DataFrame
new_data = []

for i, county in enumerate(counties):
    new_row = [''] * (len(counties) + 1)
    new_row[0] = 'ADD8E6'  # Color1 placeholder
    new_row[1] = 'FEFEDA'  # Color2 placeholder
    new_row[2] = f"{county}_test"
    new_row[i + 1] = 'x'
    new_data.append(new_row)

# Create the new DataFrame
new_df = pd.DataFrame(new_data, columns=df.columns)

# Save the new DataFrame to a CSV file
new_file_path = 'NewBeeCountyOccurrence_test.csv'
new_df.to_csv(new_file_path, index=False)

new_file_path
