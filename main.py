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
analyse = AnalyseMultiCritere('hello', 'hello')
analyse.runAnalysis()

print("--- %s seconds ---" % (time.time() - start_time))

