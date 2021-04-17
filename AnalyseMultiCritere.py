import numpy
import os
import Geoprocessing as geo
from Layer import layer
from read_csv import readCSV
import pathlib
import shutil

#
class AnalyseMultiCritere:
    # Constructeur de l'objet d'analyse multicritere qui requiert seulement 
    # une projection de référence et un extent de référence
    def __init__(self, ref_proj, ref_extent):
        self.ref_proj = ref_proj
        self.ref_extent = ref_extent
        self.envList = []
        self.physList = []
        self.ecoList = []
        self.socialList = []
        self.critereList = []
        self.mask = []

    # Remplissage des listes de facteur qui est dans le csv. 
    # Ensuite les couches se font reprojeter pour ensuite se faire rasterizer.
    # Et si nécessaire un proximity sera réaliser
    def fillFactor(self):
        print('Peuplement des facteurs......')
        test = readCSV(r'D:\dumping_codes\APPSherbrooke\source')
        self.envList = test.read_factor_layer()
        print('Peuplement des facteurs...... terminé')
    
    # Remplissage de la liste de critere qui est dans le csv. 
    # Ensuite les couches se font reprojeter pour ensuite se faire rasterizer.
    def fillCriteria(self):
        print('Peuplement des critères......')
        test = readCSV(r'D:\dumping_codes\APPSherbrooke\source')
        self.critereList = test.read_criteria_layer()
        print('Peuplement des critères...... terminé')

    # Réalisation d'un raster calculator pour toutes les couches de critère dans la liste
    # pour donner un masque final des critères.
    def calculateCriteria(self):
        print('Calcul des critère pour un masque......')
        self.mask = geo.raster_Calculator(self.critereList, r'D:\dumping_codes\APPSherbrooke\finalProduct\mask.tiff')
        print('masque...... terminé')    

    # Réalisation de la reclassifcation d'une liste de couches données pour attribuer des nouvelles valeurs 
    # selon le masque réaliser auparavant.
    def reclassifyFactor(self, liste_reclassifier):
        print('Reclassification des facteurs ............. ')
        for idx,i in enumerate(liste_reclassifier):
            i.rasPath = geo.Reclassify_Raster(i.rasPath, os.path.join(r'D:\dumping_codes\APPSherbrooke\reclassify', i.name+'.tiff'),self.mask)
        print('Reclassification .......... Terminé')

    # Réalisation du raster calculator pour une liste de couches de donnée pour donnée une couches final pour le produits final
    def calculateRaster(self, list_Calculer, axe):
        final_output = ''
        print('Calcul de tous les facteurs des facteurs ........')
        final_output = geo.raster_Calculator_factor(list_Calculer,os.path.join(r'D:\dumping_codes\APPSherbrooke\finalProduct', axe+'.tiff'))
        print('Calcul............ Terminé')

    # Réalisation de toutes les opération pour une analyse mutlicritere complete
    def runAnalysis(self):
        print("Commencement de l'analyse multicritère")
        # Portion pour les opérations sur les critères
        self.fillCriteria()
        self.calculateCriteria()
        # Portion pour les opérations sur les facteurs
        self.fillFactor()
        self.reclassifyFactor(self.envList)
        self.calculateRaster(self.envList,'enviro')
        print("Analyse multicritère........ terminé")