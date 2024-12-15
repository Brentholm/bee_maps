mn_county_map.py creates a series of png files that are maps of the state of Minnesota with counties shaded according to whether a bee occurs there. 
Reads bee data from a CSV. See MapsData2ColorTest.csv for an example. There is a header line that contains the field names. 
After that one bee per line, two colors, then species name, then the counties 
No letter means no presence, an 'x' means it's present and gets the first color, an 'n' for "new" and it gets the second color.
