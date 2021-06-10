import Geoprocessing as geo
from AnalyseMultiCritere import AnalyseMultiCritere
import pathlib
import time


# line to start the code : python 
start_time = time.time()

## sherbrooke
path = pathlib.Path().absolute()

###### main ########
geo.setUpDirectory(path)

# Set extent and projection

# Faire l'analyse mutlicritere
# parametre : 1-Projection, 2-Extent, 3-cellsize, 4-Environnement Pondération, 5-Économique Pondération, 6-Sociaux Pondération, 7-Physqiue Pondération
analyse = AnalyseMultiCritere('hello', 'hello',50)
analyse.runAnalysis()

print("--- %s minutes ---" % ((time.time() - start_time)/60))