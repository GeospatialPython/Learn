##Vector=group
##input=vector
##class_field=field input
##output=output vector
##nomodeler

from qgis.core import *
from PyQt4.QtCore import *
# import VectorWriter
try:
    # Qgis from 2.0 to 2.4
    from processing.core.VectorWriter import VectorWriter
except:
    # Qgis from 2.6
    from processing.tools.vector import VectorWriter

layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
writers = {}

class_field_index = layer.fieldNameIndex(class_field)

inFeat = QgsFeature()
outFeat = QgsFeature()
inGeom = QgsGeometry()
nElement = 0
writers = {}

feats = processing.features(layer)
nFeat = len(feats)
for inFeat in feats:
    progress.setPercentage(int(100 * nElement / nFeat))
    nElement += 1
    atMap = inFeat.attributes()
    clazz = atMap[class_field_index]
    if clazz not in writers:
        outputFile = output + '_' + str(len(writers)) + '.shp'
        writers[clazz] = VectorWriter(outputFile, None, fields,
                                      provider.geometryType(), layer.crs())
    inGeom = inFeat.geometry()
    outFeat.setGeometry(inGeom)
    outFeat.setAttributes(atMap)
    writers[clazz].addFeature(outFeat)

for writer in writers.values():
    del writer
