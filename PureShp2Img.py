"""
PureShp2Img - Convert a shapefile polygon to a PNG image using pure python

Requires Rui Carmo's PNGCanvas module from http://the.taoofmac.com
"""

import shapefile
import pngcanvas

# Read in a shapefile and write png image
r = shapefile.Reader("mississippi")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 400
iheight = 600
xratio = iwidth/xdist
yratio = iheight/ydist
pixels = []
#
# Only using the first shape record
for x,y in r.shapes()[0].points:
  px = int(iwidth - ((r.bbox[2] - x) * xratio))
  py = int((r.bbox[3] - y) * yratio)
  pixels.append([px,py])
c = pngcanvas.PNGCanvas(iwidth,iheight)
c.polyline(pixels)
f = file("mississippi.png","wb")
f.write(c.dump())
f.close()
#
# Create a world file
wld = file("mississippi.pgw", "w")
wld.write("%s\n" % (xdist/iwidth))
wld.write("0.0\n")
wld.write("0.0\n")
wld.write("-%s\n" % (ydist/iheight))
wld.write("%s\n" % r.bbox[0])
wld.write("%s\n" % r.bbox[3])
wld.close