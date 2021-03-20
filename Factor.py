
from osgeo import ogr
import gdal
import Geoprocessing as geo
import os
import shutil

# Classe pour les couches de données et faire certains prétraitement dessus pour l'Analyse multi-critère
class factor:
    def __init__(self, name,weight,path,layerName,cellsize):
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
        self.path = path
        self.layerName = layerName
        self.rasPath = ""
        self.raster = False
    
    # Rasterize les critère dans une grandeur de cellule voulu
    def setRasterLayer(self):
        extension = self.path.split('.')[1]
        if extension == 'shp':
            print('shp')
            self.rasPath = geo.Feature_to_Raster(self.path,'ESRI Shapefile',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff"),10)
            self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        elif extension == 'gdb':
            print('gdb')
            self.rasPath = geo.Feature_to_Raster(self.path,'OpenFileGDB',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff"),10,self.layerName)
            self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        else:
            shutil.copyfile(self.path,r'D:\dumping_codes\APPSherbrooke\raster')
            self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
    
    # Reclassify the raster layer with 