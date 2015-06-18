import shapefile
# Polygon shapefile we are updating.
# We must include a file extension in
# this case because the file name
# has multiple dots and pyshp would get
# confused otherwise.
file_name = "ep202009.026_5day_pgn.shp"
# Create a shapefile reader
r = shapefile.Reader(file_name)
# Create a shapefile writer
# using the same shape type
# as our reader
w = shapefile.Writer(r.shapeType)
# Copy over the existing dbf fields
w.fields = list(r.fields)
# Copy over the existing dbf records
w.records.extend(r.records())
# Copy over the existing polygons
w._shapes.extend(r.shapes())
# Add a new polygon
w.poly(parts=[[[-104,24],[-104,25],[-103,25],[-103,24],[-104,24]]])
# Add a new dbf record for our polygon making sure we include
# all of the fields in the original file (r.fields)
w.record("STANLEY","TD","091022/1500","27","21","48","ep")
# Overwrite the old shapefile or change the name and make a copy 
w.save(file_name)