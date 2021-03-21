import numpy as np
import os
import random
import shutil
import subprocess
from osgeo import ogr
from osgeo import gdal, gdal_array
from osgeo import gdalconst

# Setup les dossiers pour que le programmes fonctionne comme il le faut
def setUpDirectory(path):
    # Check if the folder of source layer
    if not os.path.exists(os.path.join(path,'source')):
        print('add the source folder for the multicriteria analysis')
    # Create folder for the raster
    if os.path.exists(os.path.join(path,'raster')):
        shutil.rmtree(os.path.join(path,'raster'))
    os.mkdir(os.path.join(path,'raster'))
    # Create folder for the finalProduct
    if os.path.exists(os.path.join(path,'finalProduct')):
        shutil.rmtree(os.path.join(path,'finalProduct'))
    os.mkdir(os.path.join(path,'finalProduct'))

# Optimisation Idée
# Ouvrir Couche de donner

# Créer Couche de données Raster

# Donne la référence spatiale

# Reprojection des couches à utiliser
def reprojection_Layer():
    #tif with projections I want
    tif = gdal.Open("/home/zeito/pyqgis_data/utah_dem4326.tif")

    #shapefile with the from projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource =   driver.Open("/home/zeito/pyqgis_data/polygon8.shp", 1)
    layer = dataSource.GetLayer()

    #set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt = tif.GetProjection())
    if sourceprj != targetprj :
        transform = osr.CoordinateTransformation(sourceprj, targetprj)
        

        to_fill = ogr.GetDriverByName("Esri Shapefile")
        ds = to_fill.CreateDataSource("/home/zeito/pyqgis_data/projected.shp")
        outlayer = ds.CreateLayer('', targetprj, ogr.wkbPolygon)
        outlayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))

        #apply transformation
        i = 0

        for feature in layer:
            transformed = feature.GetGeometryRef()
            transformed.Transform(transform)

            geom = ogr.CreateGeometryFromWkb(transformed.ExportToWkb())
            defn = outlayer.GetLayerDefn()
            feat = ogr.Feature(defn)
            feat.SetField('id', i)
            feat.SetGeometry(geom)
            outlayer.CreateFeature(feat)
            i += 1
            feat = None
        # changer parametre path pour le nouveau chemin

    ds = None
    return output

# Fonction pour effectuer un rasterize sur les fichiers vectorielle
def Feature_to_Raster(input, type_input, output_tiff, cellsize, layer="", field_name=False, NoData_value=0):
    """
    Converts a shapefile into a raster
    """
    # Chercher le driver pour la lecture
    inp_driver = ogr.GetDriverByName(type_input)
    # Lecture du fichier
    inp_source = inp_driver.Open(input, 0)
    # Si un nom de couche n'est pas donner on va chercher la premiere couche sinon on prendre celle avec le nnom
    if layer == "":
        inp_lyr = inp_source.GetLayer()
    else:
        print(layer)
        inp_lyr = inp_source.GetLayer(layer)
    # On va chercher les références spatiales de la couches
    inp_srs = inp_lyr.GetSpatialRef()

    # On établi l'extent pour chaque raster dans le processus
    # print(inp_lyr.GetExtent()) 
    x_min, x_max, y_min, y_max = (178635.17480000015, 202847.59949999955, 5018929.5001, 5043653.4749)
    x_ncells = int((x_max - x_min) / cellsize)
    y_ncells = int((y_max - y_min) / cellsize)

    # Effectue le création de fichier pour le tiff
    out_driver = gdal.GetDriverByName('GTiff')
    if os.path.exists(output_tiff):
        out_driver.Delete(output_tiff)
    out_source = out_driver.Create(output_tiff, x_ncells, y_ncells,
                                   1, gdal.GDT_Int16)
    # Tranfromation du fichier pour que ça fit un raster de la taille voulu
    out_source.SetGeoTransform((x_min, cellsize, 0, y_max, 0, -cellsize))
    out_source.SetProjection(inp_srs.ExportToWkt())
    out_lyr = out_source.GetRasterBand(1)
    #out_lyr.SetNoDataValue(NoData_value)

    # Rasterize
    if field_name:
        gdal.RasterizeLayer(out_source, [1], inp_lyr,
                            options=["ATTRIBUTE={0}".format(field_name)])
    else:
        gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[1])

    # Save and/or close the data sources
    inp_source = None
    out_source = None

    # Returne le nom du fichier 
    return output_tiff 

# Reclassify À corriger
def Reclassify_Raster(input,output,list_reclassify):
    driver = gdal.GetDriverByName('GTiff')
    file = gdal.Open(input)
    band = file.GetRasterBand(1)
    lista = band.ReadAsArray()

    # reclassification
    for j in  range(file.RasterXSize):
        for i in  range(file.RasterYSize):
            if lista[i,j] == 1:
                lista[i,j] = random.randint(1,5)
            # elif 200 < lista[i,j] < 400:
            #     lista[i,j] = 2
            # elif 400 < lista[i,j] < 600:
            #     lista[i,j] = 3
            # elif 600 < lista[i,j] < 800:
            #     lista[i,j] = 4
            # else:
            #     lista[i,j] = 5

    # Création d'un nouveau fichier pour la nouvelle reclassification
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
    # Ajout de la matrice dans le fichier
    file2.GetRasterBand(1).WriteArray(lista)

    # remet les paramèetre du fichier original
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache() 

# Raster Calculator pour les critère
def raster_Calculator(list_input, output):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    # Ouvre tous les fichiers a lire
    for i in list_input:
        print(i.rasPath)
        file = gdal.Open(i.rasPath)
        band = file.GetRasterBand(1)
        list_array.append(band.ReadAsArray())
    # Calcul tous les fichiers un apres les autres avec numpy
    for idx, i in enumerate(list_array):
        if idx == 0 :
            calc = i
        else:
            calc += i

    # create new file
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
    file2.GetRasterBand(1).WriteArray(calc)
    file2.GetRasterBand(1).SetNoDataValue(0)

    # Set Data
    band = file2.GetRasterBand(1)
    arr = band.ReadAsArray()
    arr = np.where(arr > 0, 1, arr)
    band.WriteArray(arr)       
    band.SetNoDataValue(-6999)
    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()   

# Raster Calculator pour les facteur a travailler
def raster_Calculator_factor(list_input, output, operator):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    for i in list_input:
        file = gdal.Open(i)
        band = file.GetRasterBand(1)
        list_array.append(band.ReadAsArray())

    for idx, i in enumerate(list_array):
        if idx == 0 :
            calc = (i * 0.5)
        else:
            calc = (i * 0.5)

    # create new file
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
    file2.GetRasterBand(1).WriteArray(calc)
    file2.GetRasterBand(1).SetNoDataValue(0)

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()

# Calcule la proximité du raster à partir des rasters créer du feature_to_raster
def Proximity_Raster(input, output, cellsize, layer="", field_name=False, NoData_value=0):
    """
    Converts a shapefile into a raster
    """
    # Chercher le driver pour la lecture
    driver = gdal.GetDriverByName('GTiff')
    # Lecture du fichier
    file = gdal.Open(input)
    band = file.GetRasterBand(1)
    

    # Création d'un nouveau fichier pour la nouvelle reclassification
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float32'))

    # remet les paramèetre du fichier original
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    band2 = file2.GetRasterBand(1)

    # compute the proximity
    gdal.ComputeProximity(band,band2,["VALUES=1","DISTUNITS=GEO"])
    file2.FlushCache()

# Field Calculator

# Exemple hos to run the function
Proximity_Raster(r"D:\dumping_codes\APPSherbrooke\raster\PU.tiff",r"D:\dumping_codes\APPSherbrooke\raster\ProxPU.tiff",1)