import csv
import shapefile

# Create a polygon shapefile writer
w = shapefile.Writer(shapefile.POLYGON)

# Add our fields
w.field("NAME", "C", "40")
w.field("AREA", "C", "40")

# Open the csv file and set up a reader
with open("polygons.csv") as p:
    reader = csv.DictReader(p)
    for row in reader:
        # Add records for each polygon for name and area
        w.record(row["Name"], row["Area"])
        # parse the coordinate string
        wkt = row["geometry_of_the_TT"][9:-2]
        # break the coordinate string in to x,y values
        coords = wkt.split(",")
        # set up a list to contain the coordinates
        part = []
        # convert the x,y values to floats
        for c in coords:
            x,y = c.split(" ")
            part.append([float(x),float(y)])
        # create a polygon record with the list of coordinates.
        w.poly(parts=[part])

# save the shapefile!
w.save("polys.shp")
            