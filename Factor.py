
from osgeo import ogr
import gdal

class factor:

    def __init__(self, name,weight,vecPath,layerName,cellsize):
        self.name = name
        self.weight = weight
        self.reclassifyTable = 0
        self.cellsize = cellsize
        self.Xmin = 0
        self.Xmax = 0
        self.Ymin = 0
        self.Ymax = 0
        self.fieldName = 0
        self.spatialRef = 0
        self.vecPath = vecPath
        self.layerName = layerName
        self.rasPath = ""
        self.raster = False
    
    #Set the raster path to the check if the layer is already a raster or call to create a raster
    #def setRasterLayer():