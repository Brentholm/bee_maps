mn_county_map.py creates a series of png files that are maps of the state of Minnesota with counties shaded according to whether a bee occurs there. 
Reads bee data from a CSV. See MapsData2ColorTest.csv for an example. There is a header line that contains the field names. 
After that one bee per line, two colors, then species name, then the counties 
No letter means no presence, an 'x' means it's present and gets the first color, an 'n' for "new" and it gets the second color.

generate_test_map.py is a way to make a csv containing 1 line for every county (there are 87), and when mn_county_map.py is pointed to operate from that csv, it will generate one map for each 
county, and each county's map will be shaded only for its namesake county.
for example, hennepin_test.png will be a plot that shades only Hennepin county.
