import csv
import os
from Layer import layer
# Classe pour lire les csv pour les infos de l'analyse multicritere
class readCSV:
    def __init__(self, path,cellsize):
        self.path = path
        self.cellsize = cellsize
    
    # Lecture du csv pour ajouter les couches de critères et les rasterize dans une liste pour ensuites les retourner
    def read_criteria_layer(self):
        layerlist = []
        with open(os.path.join(self.path,'source5.csv')) as csvfile:
            layerReader = csv.reader(csvfile)
            for idx,i in enumerate(layerReader):
                # Skip la premiere ligne avec les noms de colonnes
                if idx != 0:
                    # Affichage des colonnes
                    print (', '.join(i))
                    # Création de la classe
                    if i[5] != "":
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize,False,i[5])
                    else:
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize)
                    # Reprojection
                    try:
                        print('Reprojection de la couches..... '+ i[3])
                        addLayer.reprojectLayer()
                        print('Reprojection terminé')
                    except:
                        print('Reprojection échoué')
                        raise
                    # Buffer if necessary
                    try:
                        if 'Buffer' in i[6]:
                            addLayer.bufferLayer()
                    except:
                        print('Buffer échoué')
                        raise
                    # Rasterize
                    try:
                        print('Rasterize de la couches..... '+ i[3])
                        addLayer.setRasterLayer()
                        print('Rasterize terminé')
                    except:
                        print('Rasterize échoué')
                        raise
                    # Ajout à la liste
                    layerlist.append(addLayer)

        return layerlist

    # Lecture du CSV pour ajouter les couches de facteur en faisant la rasterize plus proximity si necessaire
    def read_factor_layer(self):
        bigList = []
        layerlistEnv = []
        layerlistPhys = []
        layerlistEco = []
        layerlistSoc = []
        with open(os.path.join(self.path,'source4.csv')) as csvfile:
            layerReader = csv.reader(csvfile)
            for idx,i in enumerate(layerReader):
                # Skip la premiere ligne avec les noms de colonnes
                if idx != 0:
                    # Affichage des colonnes
                    print (', '.join(i))
                    # Création de la classe
                    if i[5] != "" and i[8] != '':
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize,i[5],i[8],i[7])
                    elif i[5] != "":
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize,i[5],False,i[7])
                    elif i[8] != '':
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize,False,i[8],i[7])
                    else:
                        addLayer = layer(i[3],i[2],i[1],i[4],self.cellsize,False,False,i[7])
                    # Buffer if necessary
                    try:
                        if 'Buffer' in i[6]:
                            addLayer.bufferLayer()
                    except:
                        print('Buffer échoué')
                        raise
                    # Reprojection
                    try:
                        addLayer.reprojectLayer()
                    except:
                        print('Reprojection échoué')
                        raise
                    # Rasterize
                    try:
                        addLayer.setRasterLayer()
                    except:
                        print('Rasterize échoué')
                        raise
                    # Proximity si necessaire
                    try:
                        if 'proximity' in i[6]:
                            addLayer.setProximityLayer()
                    except:
                        print('Proximity échoué')
                        raise
                    # Ajout à la liste
                    if i[0] == 'Environnement':
                        layerlistEnv.append(addLayer)
                    elif i[0] == 'Physique':
                        layerlistPhys.append(addLayer)
                    elif i[0] == 'Social':
                        layerlistSoc.append(addLayer)
                    elif i[0] == 'Economique':
                        layerlistEco.append(addLayer)
        bigList.append(layerlistEnv)
        bigList.append(layerlistPhys)
        bigList.append(layerlistSoc)
        bigList.append(layerlistEco)
        return bigList

