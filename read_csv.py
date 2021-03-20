import csv
import os
from Factor import factor

class readCSV:
    def __init__(self, path):
        self.path = path
    
    #read csv
    def read_layer(self):
        layerlist = []
        with open(os.path.join(self.path,'source.csv')) as csvfile:
            layerReader = csv.reader(csvfile)
            for idx,i in enumerate(layerReader):
                if idx != 0:
                    print (', '.join(i))
                    addLayer = factor(i[3],i[2],i[1],i[4],10)
                    addLayer.setRasterLayer()
                    layerlist.append(addLayer)
        return layerlist


