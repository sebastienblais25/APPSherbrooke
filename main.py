import numpy
import os
import Geoprocessing as geo
from Layer import layer
from read_csv import readCSV
import geopandas
import pathlib
import shutil


## sherbrooke
path = pathlib.Path().absolute()
###### main ########
geo.setUpDirectory(path)


# Lecture des excels csv pour ajouter les fichiers ua scripts
# Lecture du csv pour les couches à utiliser pour les critères
test = readCSV(r'D:\dumping_codes\APPSherbrooke\source')
layerList = test.read_layer()
# Lectures du csv pour les facteurs

# Calcul des raster pour les critêre pour avoir un masque
geo.raster_Calculator(layerList, r'D:\dumping_codes\APPSherbrooke\finalProduct\mask.tiff')

# Utilisation du rasterize avec le proximity pour les facteurs pour un axe donnée

# Reclassification des facteur pour un axe

# Raster Calculator pour un axe

