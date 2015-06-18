import shapefile

# Create a reader instance
r = shapefile.Reader("buildingfootprints/Building_Footprint")
# Create a writer instance
w = shapefile.Writer(shapeType=shapefile.POLYGON)
# Copy the fields to the writer
w.fields = list(r.fields)
# Grab the geometry and records from all features
# with the correct county name
selection = [] 
for rec in enumerate(r.records()):
   if rec[1][1].startswith("Hancock"):
      selection.append(rec) 
# Add the geometry and records to the writer
for rec in selection:
   w._shapes.append(r.shape(rec[0]))
   w.records.append(rec[1])
# Save the new shapefile
w.save("buildingfootprints/HancockFootprints") 
