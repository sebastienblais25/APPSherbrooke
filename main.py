import numpy
import os
import Geoprocessing as geo
from AnalyseMultiCritere import AnalyseMultiCritere
from Layer import layer
from read_csv import readCSV
import pathlib
import shutil


# line to start the code : python 


## sherbrooke
path = pathlib.Path().absolute()

###### main ########
geo.setUpDirectory(path)

#Set extent and projection

# Faire l'analyse mutlicritere
analyse = AnalyseMultiCritere('hello', 'hello')
analyse.runAnalysis()

