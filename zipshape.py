"""
Example of saving a shapefile to a file-like 
object using a zip file as the target. Uses
the individual save methods for each type
of file instead of the general pyshp
save method.
"""

import zipfile
import StringIO
import shapefile

# Set up buffers for saving
shp = StringIO.StringIO()
shx = StringIO.StringIO()
dbf = StringIO.StringIO()

# Make a point shapefile
w = shapefile.Writer(shapefile.POINT)
w.point(90.3, 30)
w.point(92, 40)
w.point(-122.4, 30)
w.point(-90, 35.1)
w.field('FIRST_FLD')
w.field('SECOND_FLD','C','40')
w.record('First','Point')
w.record('Second','Point')
w.record('Third','Point')
w.record('Fourth','Point')

# Save shapefile components to buffers
w.saveShp(shp)
w.saveShx(shx)
w.saveDbf(dbf)

# Save shapefile buffers to zip file 
# Note: zlib must be available for
# ZIP_DEFLATED to compress.  Otherwise
# just use ZIP_STORED.
z = zipfile.ZipFile("myshape.zip", "w", zipfile.ZIP_DEFLATED)
z.writestr("myshape.shp", shp.getvalue())
z.writestr("myshape.shx", shx.getvalue())
z.writestr("myshape.dbf", dbf.getvalue())
z.close()

