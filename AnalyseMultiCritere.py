import os
import Geoprocessing as geo
from Layer import layer
from read_csv import readCSV
import pathlib

path = pathlib.Path().absolute()
class AnalyseMultiCritere:
    # Constructeur de l'objet d'analyse multicritere qui requiert seulement 
    # une projection de référence et un extent de référence
    def __init__(self, ref_proj, ref_extent,cellsize,envPond,socPond,ecoPond,physPond,cropdata=''):
        self.cellsize = cellsize
        self.envPond = envPond
        self.socPond = socPond
        self.ecoPond = ecoPond
        self.physPond = physPond
        self.cropdata = cropdata
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
        try:
            test = readCSV(os.path.join(path,'source'),self.cellsize)
            biglist = []
            biglist = test.read_factor_layer()
            self.envList = biglist[0]
            self.physList = biglist[1]
            self.socialList = biglist[2]
            self.ecoList = biglist[3]
        except:
            print('Peuplement des facteurs échoués')
            raise

        print('Peuplement des facteurs...... terminé')
    # Remplissage de la liste de critere qui est dans le csv. 
    # Ensuite les couches se font reprojeter pour ensuite se faire rasterizer.
    def fillCriteria(self):
        print('Peuplement des critères......')
        try:
            test = readCSV(os.path.join(path,'source'),self.cellsize)
            self.critereList = test.read_criteria_layer()
        except:
            print('Peuplement des critères échoués')
            raise

        print('Peuplement des critères...... terminé')
    # Set the Extent and projection for all the project
    def useRefProj_Extent(self):
        geo.setUpDirectory()
    # Reporject all the layer for the analysis
    def reprojectLayer(self):
        print('Reprojection des couches.........')
        try:
            for i in self.critereList:
                i.reprojectLayer()
            for i in self.ecoList:
                i.reprojectLayer()
            for i in self.envList:
                i.reprojectLayer()
            for i in self.physList:
                i.reprojectLayer()
            for i in self.socialList:
                i.reprojectLayer()
        except:
            print('rip reprojection')
        print('Reprojection des couches .........Terminé')
    # Reporject all the layer for the analysis
    def rasterizeLayer(self):
        print('Rasterization des couches..........')
        for i in self.critereList:
            i.setRasterLayer()
        for i in self.ecoList:
            i.setRasterLayer()
        for i in self.envList:
            i.setRasterLayer()
        for i in self.physList:
            i.setRasterLayer()
        for i in self.socialList:
            i.setRasterLayer()
        print('Rasterization des couches..........Terminé')
    # do the proximity process for the layers who need it
    def proximityLayers(self):
        print('Proximty process de certaines couches ...........')
        for i in self.ecoList:
            if i.proximity == True:
                print('Use Proximity')
                i.setProximityLayer()
        for i in self.envList:
            if i.proximity == True:
                print('Use Proximity')
                i.setProximityLayer()
        for i in self.physList:
            if i.proximity == True:
                print('Use Proximity')
                i.setProximityLayer()
        for i in self.socialList:
            if i.proximity == True:
                print('Use Proximity')
                i.setProximityLayer()
        print('Proximty process de certaines couches ...........Terminé')
    # Réalisation d'un raster calculator pour toutes les couches de critère dans la liste
    # pour donner un masque final des critères.
    def calculateCriteria(self):
        print('Calcul des critère pour un masque......')
        try:
            self.mask = geo.raster_Calculator(self.critereList, os.path.join(path,'intermediateProduct','mask.tiff'))
        except:
            print('Création du masque échoué')
            raise

        print('masque...... terminé')    
    # Réalisation de la reclassifcation d'une liste de couches données pour attribuer des nouvelles valeurs 
    # selon le masque réaliser auparavant.
    def reclassifyFactor(self, liste_reclassifier):
        print('Reclassification des facteurs ............. ')
        try:
            for idx,i in enumerate(liste_reclassifier):
                i.rasPath = geo.Reclassify_Raster(i.rasPath, os.path.join(path,'reclassify', i.name+'.tiff'),self.mask,i.table)
        except:
            print('Reclassification des facteurs échoués')
            raise

        print('Reclassification .......... Terminé')
    # Réalisation du raster calculator pour une liste de couches de donnée pour donnée une couches final pour le produits final
    def calculateRaster(self, list_Calculer, axe):
        final_output = ''
        print('Calcul de tous les facteurs des facteurs ........')
        try:
            final_output = geo.raster_Calculator_factor(list_Calculer,os.path.join(path,'intermediateProduct', axe+'.tiff'))
        except:
            print('Réalisation du raster calculator échoué')
            raise

        print('Calcul............ Terminé')
        return final_output
    # Réalisation de toutes les opération pour une analyse mutlicritere complete
    def runAnalysis(self):
        layerList = []
        print("Commencement de l'analyse multicritère")
        # Portion pour les opérations sur les critères
        self.fillCriteria()
        # Portion pour les opérations sur les facteurs
        self.fillFactor()
        # reproject
        self.reprojectLayer()
        #rasterize
        self.rasterizeLayer()
        # Proximity
        self.proximityLayers()
        # Create constraint mask
        self.calculateCriteria()
        # Environnement
        if len(self.envList) != 0:
            self.reclassifyFactor(self.envList)
            env = self.calculateRaster(self.envList,'enviro')
            envlayer = layer('enviro',self.envPond,env,'',self.cellsize)
            envlayer.rasPath = env
            layerList.append(envlayer)
        else:
            print("Il a aucune couche pour l'axe environnement")
        # Économique
        if len(self.ecoList) != 0:
            self.reclassifyFactor(self.ecoList)
            eco = self.calculateRaster(self.ecoList,'econo')
            ecolayer = layer('econo',self.ecoPond,eco,'',self.cellsize)
            ecolayer.rasPath = eco
            layerList.append(ecolayer)
        else:
            print("Il a aucune couche pour l'axe économique")
        # Social
        if len(self.socialList) != 0:
            self.reclassifyFactor(self.socialList)
            socio = self.calculateRaster(self.socialList,'socio')
            sociolayer = layer('socio',self.socPond,socio,'',self.cellsize)
            sociolayer.rasPath = socio
            layerList.append(sociolayer)
        else:
            print("Il a aucune couche pour l'axe social")
        # Physique
        if len(self.physList) != 0:
            self.reclassifyFactor(self.physList)
            phys = self.calculateRaster(self.physList,'phys')
            physlayer = layer('phys',self.physPond,phys,'',self.cellsize)
            physlayer.rasPath = phys
            layerList.append(physlayer)
        else:
            print("Il a aucune couche pour l'axe physique")
        print("Phase 1 ........ terminé")
        final = self.calculateRaster(layerList,'final')
        # Crop the final result
        if self.cropdata != '':
            geo.cropRaster(layerList[0].rasPath,self.cropdata,os.path.join(path,'finalProduct','ecocrop.tiff'))
            geo.cropRaster(layerList[1].rasPath,self.cropdata,os.path.join(path,'finalProduct','econocrop.tiff'))
            geo.cropRaster(layerList[2].rasPath,self.cropdata,os.path.join(path,'finalProduct','sociocrop.tiff'))
            geo.cropRaster(layerList[3].rasPath,self.cropdata,os.path.join(path,'finalProduct','physcrop.tiff'))
            geo.cropRaster(final,self.cropdata,os.path.join(path,'finalProduct','finalcrop.tiff'))
        # Sélection des sites propices Rose
        print("Analyse multicritère........ terminé")