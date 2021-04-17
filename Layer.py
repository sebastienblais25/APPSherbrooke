
from osgeo import ogr
import gdal
import Geoprocessing as geo
import os
import shutil

# Classe pour les couches de données et faire certains prétraitement dessus pour l'Analyse multi-critère
class layer:
    def __init__(self, name,weight,path,layerName,cellsize):
        self.name = name
        self.weight = weight
        self.reclassifyTable = 0
        self.fieldName = 0
        self.path = path
        self.layerName = layerName
        self.rasPath = ""
        self.raster = False

    # Reporjection des couches si besoin pour le projet
    def reprojectLayer(self):
        extension = self.path.split('.')[1]
        if extension == 'shp':
            self.path = geo.reprojection_Layer(self.path,'ESRI Shapefile')
        elif extension == 'gdb':
            self.path = geo.reprojection_Layer(self.path,'OpenFileGDB',self.layerName)

    # Rasterize les critère dans une grandeur de cellule voulu
    def setRasterLayer(self):
        extension = self.path.split('.')[1]
        if extension == 'shp':
            self.rasPath = geo.Feature_to_Raster(self.path,'ESRI Shapefile',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff"),10)
            # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        elif extension == 'gdb':
            self.rasPath = geo.Feature_to_Raster(self.path,'OpenFileGDB',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff"),10,self.layerName)
            # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
        else:
            shutil.copyfile(self.path,r'D:\dumping_codes\APPSherbrooke\raster')
            self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
    
    # Rasterize les critère dans une grandeur de cellule voulu
    def setProximityLayer(self):
        self.rasPath = geo.Proximity_Raster(self.rasPath,os.path.join(r'D:\dumping_codes\APPSherbrooke\proximity',self.name + ".tiff"),10)
        # self.rasPath = os.path.join(r'D:\dumping_codes\APPSherbrooke\raster',self.name + ".tiff")
    
    # Reclassify the raster layer with 


    # Prétraitement filtre