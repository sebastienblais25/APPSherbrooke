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
# Set extent and projection mnt_10m
proj = geo.getproj(r'D:\dumping_codes\APPSherbrooke\Ref\mnt_10m.tif')
# print(proj.GetAttrValue('AUTHORITY', 1)) mnt_10m
extent = geo.getExtent(r'D:\dumping_codes\APPSherbrooke\Ref\mnt_10m.tif')
# Faire l'analyse mutlicritere
# parametre : 1-Projection, 
#             2-Extent,
#             3-cellsize,                   Balance   Social     Environn   Économique  
#             4-Environnement Pondération, APP1==0.33 APP2==0.28 APP3==0.40 APP4==0.20 Amenagement==0.20
#             5-Économique Pondération,    APP1==0.32 APP2==0.22 APP3==0.21 APP4==0.40 Amenagement==0.40
#             6-Sociaux Pondération,       APP1==0.20 APP2==0.40 APP3==0.21 APP4==0.20 Amenagement==0.30
#             7-Physique Pondération,      APP1==0.15 APP2==0.10 APP3==0.18 APP4==0.20 Amenagement==0.15
#             8-référence pour le crop
analyse = AnalyseMultiCritere(proj, extent, 10, 0.20, 0.50, 0.20, 0.10,'source2.csv','source.csv', os.path.join(path,'Ref','municipSherb.shp'))
analyse.runAnalysis()
print("--- %s minutes ---" % ((time.time() - start_time)/60))