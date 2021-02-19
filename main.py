import numpy
import os
from osgeo import ogr
from osgeo import gdal
from osgeo import gdalconst
import pathlib

## sherbrooke
path = pathlib.Path().absolute()
###### main ########
#Check if the folder of source layer
if not os.path.exists(os.path.join(path,'source')):
    print('add the source folder for the multicriteria analysis')
#Create folder for the raster
if os.path.exists(os.path.join(path,'raster')):
    os.rmdir(os.path.join(path,'raster'))
os.mkdir(os.path.join(path,'raster'))
    
