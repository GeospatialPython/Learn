"""
shp2img.py - creates a png image and world file (.pgw) from a shapefile
containing a single polygon.
author: jlawhead@geospatialpyton.com
date: 20101204

This script requires the Python Imaging Library.
The sample shapefile used is available at:
http://geospatialpython.googlecode.com/files/Mississippi.zip
"""

import shapefile
import Image, ImageDraw

# Read in a shapefile
r = shapefile.Reader("mississippi")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 400
iheight = 600
xratio = iwidth/xdist
yratio = iheight/ydist
pixels = []
for x,y in r.shapes()[0].points:
  px = int(iwidth - ((r.bbox[2] - x) * xratio))
  py = int((r.bbox[3] - y) * yratio)
  pixels.append((px,py))
img = Image.new("RGB", (iwidth, iheight), "white")
draw = ImageDraw.Draw(img)
draw.polygon(pixels, outline="rgb(203, 196, 190)", fill="rgb(198, 204, 189)")
img.save("mississippi.png")

# Create a world file
wld = file("mississippi.pgw", "w")
wld.write("%s\n" % (xdist/iwidth))
wld.write("0.0\n")
wld.write("0.0\n")
wld.write("-%s\n" % (ydist/iheight))
wld.write("%s\n" % r.bbox[0])
wld.write("%s\n" % r.bbox[3])
wld.close