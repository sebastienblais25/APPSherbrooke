
from osgeo import ogr
import gdal
import Geoprocessing as geo
import os
import shutil
import pathlib

## sherbrooke
path = pathlib.Path().absolute()

# Classe pour les couches de données et faire certains prétraitement dessus pour l'Analyse multi-critère
class layer:
    def __init__(self, name,weight,path,layerName,cellsize,burnValue=False,fieldname=False,table=''):
        self.name = name
        self.weight = weight
        self.fieldName = fieldname
        self.path = path
        self.layerName = layerName
        self.rasPath = ""
        self.raster = False
        self.burnValue = burnValue
        self.cellsize = cellsize
        self.table = table
        self.proximity = False
        self.buffer = False

    # set the proximity to true
    def proximityProcess(self):
        self.proximity = True

    # Reporjection des couches si besoin pour le projet
    def reprojectLayer(self):
        extension = self.path.split('.')[1]
        if extension == 'shp':
            self.path = geo.reprojection_Layer(self.path,'ESRI Shapefile')
        elif extension == 'gdb':
            self.path = geo.reprojection_Layer(self.path,'OpenFileGDB',self.layerName)
        elif extension == "gpkg":
            self.path = geo.reprojection_Layer(self.path,'GPKG',self.layerName)
        elif extension == "tif":
            self.path = geo.reprojectRaster(self.path,os.path.join(path,'reproject',self.name+".tiff"),'EPSG:32187',self.cellsize)

    # Rasterize les critère dans une grandeur de cellule voulu
    def setRasterLayer(self):
        extension = self.path.split('.')[1]
        if extension == 'shp':
            self.rasPath = geo.Feature_to_Raster(self.path,'ESRI Shapefile',os.path.join(path,'raster',self.name + ".tiff"),self.cellsize,'',self.burnValue,self.fieldName)
            # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        elif extension == 'gdb':
            self.rasPath = geo.Feature_to_Raster(self.path,'OpenFileGDB',os.path.join(path,'raster',self.name + ".tiff"),self.cellsize,self.layerName,self.burnValue,self.fieldName)
            # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        elif extension == 'gpkg':
            self.rasPath = geo.Feature_to_Raster(self.path,'GPKG',os.path.join(path,'raster',self.name + ".tiff"),self.cellsize,self.layerName,self.burnValue,self.fieldName)
            # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        else:
            shutil.copyfile(self.path, os.path.join(path,'raster',self.name+ ".tiff"))
            self.rasPath = os.path.join(path,'raster',self.name + ".tiff")
    
    # Rasterize les critère dans une grandeur de cellule voulu
    def setProximityLayer(self):
        self.rasPath = geo.Proximity_Raster(self.rasPath,os.path.join(path,'proximity',self.name + ".tiff"))
        # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
    
    # Mets un buffer sur couches qui n'est pas un polygone
    def bufferLayer(self):
        self.path = geo.bufferLineAndPoints(self.path,os.path.join(r'D:\dumping_codes\APPSherbrooke\buffer',self.name+'.shp'),1,self.layerName)
    
    # Reclassify the raster layer with
    # Prétraitement filtre