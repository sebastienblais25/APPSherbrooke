import Geoprocessing as geo
from AnalyseMultiCritere import AnalyseMultiCritere
import pathlib
import time
import os


# line to start the code : python 
start_time = time.time()

## sherbrooke
path = pathlib.Path().absolute()

###### main ########
geo.setUpDirectory(path)

# Set extent and projection

# Faire l'analyse mutlicritere
# parametre : 1-Projection, 
#             2-Extent,
#             3-cellsize,
#             4-Environnement Pondération, 
#             5-Économique Pondération,
#             6-Sociaux Pondération, 
#             7-Physique Pondération, 
#             8-référence pour le crop
analyse = AnalyseMultiCritere('hello', 'hello', 10, 0.33, 0.25, 0.27, 0.15, os.path.join(path,'APP_data','municipSherb.shp'))
analyse.runAnalysis()

print("--- %s minutes ---" % ((time.time() - start_time)/60))