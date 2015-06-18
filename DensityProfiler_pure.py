import random
import shapefile
import pngcanvas

def pip(x,y,poly):
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

# Source shapefile
r = shapefile.Reader("GIS_CensusTract_poly.shp")

# pixel to coordinate info
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 600
iheight = 500
xratio = iwidth/xdist
yratio = iheight/ydist

c = pngcanvas.PNGCanvas(iwidth,iheight,color=[255,255,255,0xff])

# background color
c.filledRectangle(0,0,iwidth,iheight)

# Pen color
c.color = [139,137,137,0xff]

# Draw the polygons 
for shape in r.shapes():
  pixels = []
  for x,y in shape.points:  
    px = int(iwidth - ((r.bbox[2] - x) * xratio))
    py = int((r.bbox[3] - y) * yratio)
    pixels.append([px,py])
  c.polyline(pixels)

rnum = 0
trnum = len(r.shapeRecords())
for sr in r.shapeRecords():
  rnum += 1
  #print rnum, " of ", trnum
  density = sr.record[20]
  total = int(density / 50)
  count = 0
  minx, miny, maxx, maxy = sr.shape.bbox   
  while count < total:    
    x = random.uniform(minx,maxx)
    y = random.uniform(miny,maxy)    
    if pip(x,y,sr.shape.points):
      count += 1
      #print " ", count, " of ", total
      px = int(iwidth - ((r.bbox[2] - x) * xratio))
      py = int((r.bbox[3] - y) * yratio)
      c.point(px,py,color=[255,0,0,0xff])

f = file("density_pure.png", "wb")
f.write(c.dump())
f.close()
        