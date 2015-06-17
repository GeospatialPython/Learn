from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

class MapComposer:
	"""PyQGIS Composer class.  Encapsulates boiler plate QgsComposition
	code and centers the QgsComposerMap object on an 8.5x11 inch page."""
	def __init__(self, qmlr=None, qmr=None, **kwargs):
		self.paperWidth = 215.9
		self.paperHeight = 279.4
		self.rectScale = 1.2
		self.xScale = .5
		self.yScale = .5
		self.qmlr = qmlr
		self.qmr = qmr
		self.__dict__.update(kwargs)			
		self.lyrs = self.qmlr.mapLayers().keys()
		self.qmr.setLayerSet(self.lyrs)
		self.rect = QgsRectangle(self.qmr.extent())
		self.rect.scale(self.rectScale)
		self.qmr.setExtent(self.rect)
		self.c = QgsComposition(self.qmr)
		self.c.setPlotStyle(QgsComposition.Print)
		self.c.setPaperSize(self.paperWidth, self.paperHeight)
		self.w = self.c.paperWidth() * self.xScale
		self.h = self.c.paperHeight() * self.yScale
		self.x = (self.c.paperWidth() - self.w) / 2
		self.y = (self.c.paperHeight() - self.h) / 2
		self.composerMap = QgsComposerMap(self.c,self.x,self.y,self.w,self.h)
		self.composerMap.setNewExtent(self.rect)		
		self.composerMap.setFrameEnabled(True)
		self.c.addItem(self.composerMap)

	def output(self, path, format):
		self.dpi = self.c.printResolution()
		self.c.setPrintResolution(self.dpi)
		self.dpmm = self.dpi / 25.4
		self.width = int(self.dpmm * self.c.paperWidth())
		self.height = int(self.dpmm * self.c.paperHeight())
		self.image = QImage(QSize(self.width, self.height), QImage.Format_ARGB32)
		self.image.setDotsPerMeterX(self.dpmm * 1000)
		self.image.setDotsPerMeterY(self.dpmm * 1000)
		self.image.fill(0)
		self.imagePainter = QPainter(self.image)
		self.sourceArea = QRectF(0, 0, self.c.paperWidth(), self.c.paperHeight())
		self.targetArea = QRectF(0, 0, self.width, self.height)
		self.c.render(self.imagePainter, self.targetArea, self.sourceArea)
		self.imagePainter.end()
		self.image.save(path, format)		
