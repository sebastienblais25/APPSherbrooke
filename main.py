import numpy
import os
import Geoprocessing as geo
from Factor import factor
from read_csv import readCSV
import geopandas
import pathlib
import shutil


## sherbrooke
path = pathlib.Path().absolute()
###### main ########
geo.setUpDirectory(path)

#Read the CSV file for the list of layer to use
test = readCSV(r'D:\dumping_codes\APPSherbrooke\source')
layerList = test.read_layer()

geo.raster_Calculator(layerList, r'D:\dumping_codes\APPSherbrooke\finalProduct\mask.tiff')


# geo.Feature_to_Raster(layer.vecPath,'ESRI Shapefile',r'D:\dumping_codes\APPSherbrooke\raster\test.tiff',50)

# geo.Reclassify_Raster(r'D:\dumping_codes\APPSherbrooke\raster\test.tiff', r'D:\dumping_codes\APPSherbrooke\raster\testReclassify.tiff')
# list_input = []
# list_input.append(r'D:\dumping_codes\APPSherbrooke\raster\test.tiff')
# list_input.append(r'D:\dumping_codes\APPSherbrooke\raster\testReclassify.tiff')

# geo.raster_Calculator(list_input,r'D:\dumping_codes\APPSherbrooke\raster\testCalc.tiff','+')
