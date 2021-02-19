
from osgeo import ogr
import gdal

class factor
    __init__(self, name,weight,reclassifyTable,cellsize,Xmin,Xmax,Ymin,Ymax,fieldName,spatialRef,vecPath,layerName):
        self.name = name
        self.weight = weight
        self.reclassifyTable = reclassifytable
        self.cellsize = cellsize
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Ymin = Ymin
        self.Ymax = Ymax
        self.fieldName = fieldName
        self.spatialRef = spatialRef
        self.vecPath = vecPath
        self.layerName = layerName
        self.rasPath = ""
        self.raster = false
    
    #Set the raster path to the check if the layer is already a raster or call to create a raster
    def setRasterLayer():