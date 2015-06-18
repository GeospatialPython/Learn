import cStringIO
import struct
import shapefile
import random
import time

class LargeWriter:
  def __init__(self, filename=None, shapeType=1, hasShx=True):
    self.filename = filename
    self.hasShx = hasShx
    # Count records for metadata
    self.count = 0
    # Maximum number of records before disk flush
    self.max = 1000
    self.started = False
    self.minx = 0
    self.miny = 0
    self.maxx = 0
    self.maxy = 0
    self.numRecs = 0
    self.tmpShp = cStringIO.StringIO()
    if self.hasShx:
      self.tmpShx = cStringIO.StringIO()
    self.tmpDbf = cStringIO.StringIO()
    self.shp = open("%s.shp" % self.filename, "wb")
    if self.hasShx:
      self.shx = open("%s.shx" % self.filename, "wb")
    self.dbf = open("%s.dbf" % self.filename, "wb")
    self.dbfHdrLen = 0
    self.w = shapefile.Writer(shapeType)

  def endcap(self):
        """First and last batches"""
        self.started = True
        self.tmpShp.seek(36)
        self.xmin = struct.unpack("<d", self.tmpShp.read(8))[0]
        self.ymin = struct.unpack("<d", self.tmpShp.read(8))[0]
        self.xmax = struct.unpack("<d", self.tmpShp.read(8))[0]
        self.ymax = struct.unpack("<d", self.tmpShp.read(8))[0]        
        self.tmpShp.seek(0)
        if self.hasShx:
          self.tmpShx.seek(0)
        self.tmpDbf.seek(8)
        # The length of the dbf header will not change
        self.dbfHdrLen = struct.unpack("<H", self.tmpDbf.read(2))[0]
        self.tmpDbf.seek(0)
        self.shp.write(self.tmpShp.read())
        if self.hasShx:
          self.shx.write(self.tmpShx.read())
        self.dbf.write(self.tmpDbf.read())

  def batch(self):
        self.started = True
        # Update shx offsets
        if self.hasShx:
          self.tmpShx.seek(0,2)
          shxsz = self.tmpShx.tell()
          shxcur = 100
          adder = self.shx.tell() / 2
          self.tmpShx.seek(100) 
          while shxcur < shxsz:         
            offset = struct.unpack(">i", self.tmpShx.read(4))[0]
            newOffset = adder + offset
            self.tmpShx.seek(-4, 1)
            self.tmpShx.write(struct.pack(">i", newOffset))
            self.tmpShx.seek(8, 1)
            shxcur = self.tmpShx.tell()
        # Get shp bounding box
        self.tmpShp.seek(36)
        xmin = struct.unpack("<d", self.tmpShp.read(8))[0]
        ymin = struct.unpack("<d", self.tmpShp.read(8))[0]
        xmax = struct.unpack("<d", self.tmpShp.read(8))[0]
        ymax = struct.unpack("<d", self.tmpShp.read(8))[0]
        self.xmin = min([self.xmin, xmin])
        self.ymin = min([self.ymin, ymin])
        self.xmax = max([self.xmax, xmax])
        self.ymax = max([self.ymax, ymax])
        self.tmpShp.seek(100)
        self.tmpShx.seek(100)
        self.tmpDbf.seek(self.dbfHdrLen)       
        self.shp.write(self.tmpShp.read())
        if self.hasShx:
          self.shx.write(self.tmpShx.read())
        self.dbf.write(self.tmpDbf.read())
  
  def record(self, *recordList):
    """Count the records and save them"""
    self.count += 1
    self.numRecs += 1
    apply(self.w.record, recordList)
    if self.count >= self.max:
      if self.hasShx:
        self.w.save(shp=self.tmpShp, shx=self.tmpShx, dbf=self.tmpDbf)
      else:
        self.w.save(shp=self.tmpShp, dbf=self.tmpDbf)  
      if not self.started:
        self.endcap()
      else:
        self.batch()
      # Reset the buffers for the next batch
      self.tmpShp = cStringIO.StringIO()
      if self.hasShx:
        self.tmpShx = cStringIO.StringIO()
      self.tmpDbf = cStringIO.StringIO()
      self.count = 0
        
  def save(self):
    self.shp.seek(0,2)
    shpLength = self.shp.tell() / 2
    self.shp.seek(24)
    self.shp.write(struct.pack(">i", shpLength))
    self.shp.seek(36)
    self.shp.write(struct.pack("<4d", self.xmin,self.ymin,self.xmax,self.ymax))
    if self.hasShx:        
      self.shx.seek(0,2)   
      shxLength = self.shx.tell() / 2   
      self.shx.seek(24)
      self.shx.write(struct.pack(">i", shxLength))
      self.shx.seek(36)
      self.shx.write(struct.pack("<4d", self.xmin,self.ymin,self.xmax,self.ymax))          
    # update dbf record count
    self.dbf.seek(4)
    self.dbf.write(struct.pack("<L", self.numRecs))
    self.shp.close()
    if self.hasShx:
      self.shx.close()
    self.dbf.close()        
        
def random_point():
  """returns a randomly generated point"""
  x = random.uniform(-180,180)
  y = random.uniform(-90,90)
  return x,y

def progress(last, count, total):
  """Print percent completed"""
  percent = int((count/(total*1.0))*100.0)
  if percent % 10.0 == 0 and percent > last:
    print "%s %% done - Shape %s/%s at %s" % (percent, count, total, time.asctime())
  return percent  


# Create a large shapefile writer with
# a filname and a shapefile type.
# 1=Point, 5=Polygon
lw = LargeWriter("giantShp", 1, hasShx=True)
#lw = LargeWriter("giantShp", 1, hasShx=False)

# Add some dbf fields
lw.w.field("ID", "C", "40")
lw.w.field("X", "C", "40")
lw.w.field("Y", "C", "40")

# Progress counter
status = 0

# Number of random points to write
total = 107374177

for i in range(total):
  # Progress meter
  status = progress(status, i, total)
  # Generate a random point
  x,y = random_point()
  x1,y1 = random_point()
  x2,y2 = random_point()
  x3,y3 = random_point()
  x4,y4 = random_point()      
  # Call the shapefile point() method 
  lw.w.point(x,y)
  # Call the specialized record method
  lw.record(i,x,y)
  #lw.w.poly(parts=[[[x,y],[x1,y1],[x2,y2],[x3,y3],[x4,y4]]])
  #lw.record(i,x,y)
  #x,y = random_point()
  #x1,y1 = random_point()
  #x2,y2 = random_point()
  #x3,y3 = random_point()
  #x4,y4 = random_point()      
  #Call the shapefile poly() method 
  #lw.w.poly(parts=[[[x,y],[x1,y1],[x2,y2],[x3,y3],[x4,y4]]])
  #Call the specialized record method
  #lw.record(i,x,y) 

# Special LargeWriter save method
lw.save()    