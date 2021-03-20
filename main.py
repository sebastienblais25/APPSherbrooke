import numpy
import os
import Geoprocessing as geo
from Factor import factor
import geopandas
import pathlib
import shutil


## sherbrooke
path = pathlib.Path().absolute()
###### main ########
#Check if the folder of source layer
if not os.path.exists(os.path.join(path,'source')):
    print('add the source folder for the multicriteria analysis')
# Create folder for the raster
if os.path.exists(os.path.join(path,'raster')):
    shutil.rmtree(os.path.join(path,'raster'))
os.mkdir(os.path.join(path,'raster'))
#


layer = factor("test", 0.3 ,r"D:\APP_data\zone_analyse_parcindustriel.shp","dump",1)

geo.Feature_to_Raster(layer.vecPath,'ESRI Shapefile',r'D:\dumping_codes\APPSherbrooke\raster\test.tiff',50)

geo.Reclassify_Raster(r'D:\dumping_codes\APPSherbrooke\raster\test.tiff', r'D:\dumping_codes\APPSherbrooke\raster\testReclassify.tiff')
list_input= []
list_input.append(r'D:\dumping_codes\APPSherbrooke\raster\test.tiff')
list_input.append(r'D:\dumping_codes\APPSherbrooke\raster\testReclassify.tiff')

geo.raster_Calculator(list_input,r'D:\dumping_codes\APPSherbrooke\raster\testCalc.tiff','+')
