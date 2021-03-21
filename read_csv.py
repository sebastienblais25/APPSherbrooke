import csv
import os
from Layer import layer
# Classe pour lire les csv pour les infos de l'analyse multicritere
class readCSV:
    def __init__(self, path):
        self.path = path
    
    # Lecture du csv pour ajouter les couches de critères et les rasteriz edans une liste pour ensuites les retourner
    def read_layer(self):
        layerlist = []
        with open(os.path.join(self.path,'source.csv')) as csvfile:
            layerReader = csv.reader(csvfile)
            for idx,i in enumerate(layerReader):
                # Skip la premiere ligne avec les noms de colonnes
                if idx != 0:
                    # Affichage des colonnes
                    print (', '.join(i))
                    # Création de la classe
                    addLayer = layer(i[3],i[2],i[1],i[4],10)
                    # Rasterize
                    addLayer.setRasterLayer()
                    # Ajout à la liste
                    layerlist.append(addLayer)
        return layerlist


