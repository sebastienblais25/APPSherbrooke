import os
import pathlib
import shutil
import numpy as np
import whitebox
from osgeo import gdal, ogr, osr

path = pathlib.Path().absolute()

# Setup les dossiers pour que le programmes fonctionne comme il le faut
def setUpDirectory(path):
    # Check if the folder of source layer
    try:
        if not os.path.exists(os.path.join(path,'source')):
            print('add the source folder for the multicriteria analysis')
    except:
        print('Fichier est ouvert')
        raise
    # Create folder for the raster
    try:
        if os.path.exists(os.path.join(path,'raster')):
            shutil.rmtree(os.path.join(path,'raster'))
        os.mkdir(os.path.join(path,'raster'))
    except:
        print('Fichier raster est ouvert')
        raise
    # Create folder for the raster
    try:
        if os.path.exists(os.path.join(path,'proximity')):
            shutil.rmtree(os.path.join(path,'proximity'))
        os.mkdir(os.path.join(path,'proximity'))
    except:
        print('fichier raster est ouvert')
        raise
    # Create folder for the intermediateProduct
    try:
        if os.path.exists(os.path.join(path,'intermediateProduct')):
            shutil.rmtree(os.path.join(path,'intermediateProduct'))
        os.mkdir(os.path.join(path,'intermediateProduct'))
    except:
        print('Fichier intermediateProduct est ouvert')
        raise
    # Create folder for the finalProduct
    try:
        if os.path.exists(os.path.join(path,'finalProduct')):
            shutil.rmtree(os.path.join(path,'finalProduct'))
        os.mkdir(os.path.join(path,'finalProduct'))
    except:
        print('Fichier finalProduct est ouvert')
        raise
    # Create folder for the reproject
    try:
        if os.path.exists(os.path.join(path,'reproject')):
            shutil.rmtree(os.path.join(path,'reproject'))
        os.mkdir(os.path.join(path,'reproject'))
    except:
        print('Fichier reproject est ouvert')
        raise
    # Create folder for the reclassify
    try:
        if os.path.exists(os.path.join(path,'reclassify')):
            shutil.rmtree(os.path.join(path,'reclassify'))
        os.mkdir(os.path.join(path,'reclassify'))
    except:
        print('Fichier reclassify est ouvert')
        raise

# Clean tous les dossier pour prendre l moins d'espace possible
def cleanUpDirectory(path):
    # Delete Folder
    try:
        shutil.rmtree(os.path.join(path,'raster'))
        shutil.rmtree(os.path.join(path,'proximity'))
        shutil.rmtree(os.path.join(path,'reproject'))
    except:
        print('Fichier raster ou proximity ou reproject ouvert')
        raise

# Permet de mettre un petit buffer autour des objet qui ne sont pas des polygones pour réaliser un rasterize
def bufferLineAndPoints(inputfn, outputBufferfn, bufferDist,layername):
    try:
        inputds = ogr.Open(inputfn)
        inputlyr = inputds.GetLayer(layername)

        shpdriver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(outputBufferfn):
            shpdriver.DeleteDataSource(outputBufferfn)
        outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
        bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
        featureDefn = bufferlyr.GetLayerDefn()
    except:
        print('Accèes a la couche impossible')
        raise

    try:
        for feature in inputlyr:
            ingeom = feature.GetGeometryRef()
            geomBuffer = ingeom.Buffer(bufferDist)

            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(geomBuffer)
            bufferlyr.CreateFeature(outFeature)
    except:
        print('Application du buffer échoué')
        raise

    try:
        bufferlyr.SetProjection(inputlyr.GetSpatialRef().ExportToWkt())
    except:
        print('Échec de la définition de la projection')
        raise

    ds = None
    return outputBufferfn

# Donne l'extent de référence
def getExtent(input):
    try:
        ds = gdal.Open(input)
        xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
        width, height = ds.RasterXSize, ds.RasterYSize
        xmax = xmin + width * xpixel
        ymin = ymax + height * ypixel
    except:
        raise ('Extent introuvable')

    return (xmin,xmax,ymin,ymax)

# Donne la référence spatiale de référence
def getproj(input):
    try :
        file = gdal.Open(input)
        proj = osr.SpatialReference(wkt=file.GetProjection())
    except:
        raise ('Référence spatiale introuvable')
    return proj

# Reprojection des couches à utiliser
def reprojection_Layer(proj, input, typefile, layer=""):

    # read Layer
    try:
        driver = ogr.GetDriverByName(typefile)
        dataSource = driver.Open(input, 0)
        if layer == "":
            inp_lyr = dataSource.GetLayer()
        else:
            inp_lyr = dataSource.GetLayer(layer)
    
        output = input
    except:
        print('Couche impossible a lire')
        raise

    #set spatial reference and transformation
    try:
        sourceprj = inp_lyr.GetSpatialRef()
    # les path sont a changer sont hardcoder
        if sourceprj != proj:
            if layer == "":
                output = os.path.join(path,"reproject", input.split("\\")[-1])
            else:
                output = os.path.join(path,"reproject", layer + '.shp')
            transform = osr.CoordinateTransformation(sourceprj, proj)
        
            to_fill = ogr.GetDriverByName("Esri Shapefile")
            ds = to_fill.CreateDataSource(output)
            outlayer = ds.CreateLayer('', proj, ogr.wkbPolygon)
            #outlayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
            fields = [field.name for field in inp_lyr.schema]
            for i in fields:
                outlayer.CreateField(ogr.FieldDefn(i, ogr.OFTString))
    except:
        print('Impossible de définir une référence et une transformation')
        raise

    #apply transformation
    i = 0
    try:
        for feature in inp_lyr:
            transformed = feature.GetGeometryRef()
            transformed.Transform(transform)

            geom = ogr.CreateGeometryFromWkb(transformed.ExportToWkb())
            defn = outlayer.GetLayerDefn()
            feat = ogr.Feature(defn)
            #feat.SetField('id', i)
            for idx, outfield in enumerate(outlayer.schema):
                try:
                    feat.SetField(feat.GetFieldIndex(outfield.name), str(feature.GetField(inp_lyr.schema[idx].name)))
                except:
                    pass
            feat.SetGeometry(geom)
            outlayer.CreateFeature(feat)
            i += 1
            feat = None
    except:
        print('Transformation échoué')
        raise
    # changer parametre path pour le nouveau chemin

    ds = None
    return output

# Fonction pour effectuer un rasterize sur les fichiers vectorielle
def Feature_to_Raster(extentinp, input, type_input, output_tiff, cellsize, layer="", burnvalue=False, field_name=False, NoData_value=0):
    """
    Converts a shapefile into a raster
    """
    try:
        # Chercher le driver pour la lecture
        inp_driver = ogr.GetDriverByName(type_input)
        # Lecture du fichier
        inp_source = inp_driver.Open(input, 0)
        # Si un nom de couche n'est pas donner on va chercher la premiere couche sinon on prendre celle avec le nnom
        if layer == "":
            inp_lyr = inp_source.GetLayer()
        else:
            inp_lyr = inp_source.GetLayer(layer)
    except:
        print('Impossible to read the layer')
        raise
    # On va chercher les références spatiales de la couches
    try:
        inp_srs = inp_lyr.GetSpatialRef()
    except:
        print('Référence spatiales introuvable')
        raise

    # On établi l'extent pour chaque raster dans le processus
    # print(inp_lyr.GetExtent())
    try:
        x_min, x_max, y_min, y_max = extentinp
        x_ncells = int((x_max - x_min) / cellsize)
        y_ncells = int((y_max - y_min) / cellsize)
    except:
        print('erreur dans la définition de extent')
        raise

    # Effectue le création de fichier pour le tiff
    try:
        out_driver = gdal.GetDriverByName('GTiff')
        if os.path.exists(output_tiff):
            out_driver.Delete(output_tiff)
        out_source = out_driver.Create(output_tiff, x_ncells, y_ncells,
                                    1, gdal.GDT_Float64)
    except:
        print('Échec de la création du fichier pour le tiff')
        raise

    # Tranfromation du fichier pour que ça fit un raster de la taille voulu
    try:
        out_source.SetGeoTransform((x_min, cellsize, 0, y_max, 0, -cellsize))
        out_source.SetProjection(inp_srs.ExportToWkt())
        out_lyr = out_source.GetRasterBand(1)
    except:
        print('Échec de la transformation du fichier')
        raise
    

    # Rasterize
    try:
        if field_name:
            out_lyr.SetNoDataValue(NoData_value)
            inp_lyr.SetAttributeFilter(field_name)
            gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[1])
        elif burnvalue:
            out_lyr.SetNoDataValue(-6999)
            gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[255],options = ["ATTRIBUTE=%s" % burnvalue])
        else:
            out_lyr.SetNoDataValue(NoData_value)
            gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[1])

        # Save and/or close the data sources
        inp_source = None
        out_source = None
    except:
        print('Erreur avec la fonction Rasterize')
        raise

    # Returne le nom du fichier 
    return output_tiff 

# Reclassify À corriger
def Reclassify_Raster(input,output, maskin,table):
    # open layer
    try:
        driver = gdal.GetDriverByName('GTiff')
        file = gdal.Open(input)
        band = file.GetRasterBand(1)
        lista = band.ReadAsArray()
    except:
        print('Couche impossible a ouvrir')
        raise

    # mask layer
    try:
        mask= gdal.Open(maskin)
        bandmask = mask.GetRasterBand(1)
        listMask = bandmask.ReadAsArray()
        reclassif = table.split(';')
    except:
        print('Couche du mask impossible a ouvrir')
        raise

    # reclassification
    try:
        if reclassif[0] != 'no':
            for j in  range(file.RasterXSize):
                for i in  range(file.RasterYSize):
                    if lista[i,j] <= int(reclassif[0].split(':')[0]):
                        if listMask[i,j] == 0:
                            lista[i,j] = float(reclassif[0].split(':')[1])
                        else:
                            lista[i,j] = 0
                    elif lista[i,j] <= int(reclassif[1].split(':')[0]):
                        if listMask[i,j] == 0:
                            lista[i,j] = float(reclassif[1].split(':')[1])
                        else:
                            lista[i,j] = 0
                    elif lista[i,j] <= int(reclassif[2].split(':')[0]):
                        if listMask[i,j] == 0:
                            lista[i,j] = float(reclassif[2].split(':')[1])
                        else:
                            lista[i,j] = 0
                    elif lista[i,j] <= int(reclassif[3].split(':')[0]):
                        if listMask[i,j] == 0:
                            lista[i,j] = float(reclassif[3].split(':')[1])
                        else:
                            lista[i,j] = 0
                    elif lista[i,j] >= int(reclassif[4].split(':')[0]):
                        if listMask[i,j] == 0:
                            lista[i,j] = float(reclassif[4].split(':')[1])
                        else:
                            lista[i,j] = 0
                    else:
                        lista[i,j] = 0
        else:
            for j in  range(file.RasterXSize):
                for i in  range(file.RasterYSize):
                    if listMask[i,j] == 1 or listMask[i,j] < 0:
                            lista[i,j] = 0
    except:
        print('Reclassification échoué')
        raise

    # Création d'un nouveau fichier pour la nouvelle reclassification
    try:
        file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float64'))
    except:
        print('Création du nouveau fichier pour la reclassification impossible')
        raise
    # Ajout de la matrice dans le fichier
    try:
        file2.GetRasterBand(1).WriteArray(lista)
    except:
        print('Ajout de la matrice au fichier impossible')
        raise

    # remet les paramèetre du fichier original
    try:
        proj = file.GetProjection()
        georef = file.GetGeoTransform()
        file2.SetProjection(proj)
        file2.SetGeoTransform(georef)
        file2.FlushCache()
    except:
        print('Impossible de remettre les paramètre du fichier original')
        raise

    return output

# Raster Calculator pour les critère
def raster_Calculator(list_input, output):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    # Ouvre tous les fichiers a lire
    try:
        for i in list_input:
            file = gdal.Open(i.rasPath)
            band = file.GetRasterBand(1)
            list_array.append(band.ReadAsArray())
    except:
        print('Ouverture de un ou plusieur fichiers impossible')
        raise

    # Calcul tous les fichiers un apres les autres avec numpy
    try:
        for idx, i in enumerate(list_array):
            if idx == 0 :
                calc = i
            else:
                calc += i
    except:
        print('Calcule de tous les fichiers avec numpy échoué')
        raise

    # create new file
    try:
        file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
        file2.GetRasterBand(1).WriteArray(calc)
        file2.GetRasterBand(1).SetNoDataValue(0)
    except:
        print('Création des nouveaux fichiers échoués')
        raise

    # Set Data
    try:
        band = file2.GetRasterBand(1)
        arr = band.ReadAsArray()
        arr = np.where(arr > 0, 1, arr)
        band.WriteArray(arr)
        band.SetNoDataValue(-6999)
    except:
        print('Définition des données échoués')
        raise
    # spatial ref system
    try:
        proj = file.GetProjection()
        georef = file.GetGeoTransform()
        file2.SetProjection(proj)
        file2.SetGeoTransform(georef)
        file2.FlushCache()
    except:
        print('Erreur avec le système de référence')
        raise

    return output

# Raster Calculator pour les facteur a travailler
def raster_Calculator_factor(list_input, output):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    try:
        for i in list_input:
            file = gdal.Open(i.rasPath)
            band = file.GetRasterBand(1)
            list_array.append(band.ReadAsArray())
    except:
        print('Ouverture de un ou plusieur fichiers impossible')
        raise

    try:
        for idx, i in enumerate(list_array):
            if idx == 0 :
                calc = (i * float(list_input[idx].weight))
            else:
                calc += (i * float(list_input[idx].weight))
    except:
        print('Calcule de tout les fichiers avec numpy échoués')
        raise

    # create new file
    try:
        print(output)
        file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float64'))
        file2.GetRasterBand(1).WriteArray(calc)
        file2.GetRasterBand(1).SetNoDataValue(0)
    except:
        print('Création des nouveaux fichiers échoués')
        raise

    # spatial ref system
    try:
        proj = file.GetProjection()
        georef = file.GetGeoTransform()
        file2.SetProjection(proj)
        file2.SetGeoTransform(georef)
        file2.FlushCache()
    except:
        print('Erreur avec le système de référence')
        raise

    return output

# Calcule la proximité du raster à partir des rasters créer du feature_to_raster
def Proximity_Raster(input, output):
    """
    Converts a shapefile into a raster
    """
    # Chercher le driver pour la lecture
    try:
        driver = gdal.GetDriverByName('GTiff')
    except:
        print('Driver introuvable')
        raise
    # Lecture du fichier
    try:
        file = gdal.Open(input)
        band = file.GetRasterBand(1)
    except:
        print('Échec de la lecture du fichier')
        raise
    

    # Création d'un nouveau fichier pour la nouvelle reclassification
    try:
        file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float64'))
    except:
        print('Échec de la création du nouveau fichier pour la nouvelle reclassification')
        raise

    # remet les paramèetre du fichier original
    try:
        proj = file.GetProjection()
        georef = file.GetGeoTransform()
        file2.SetProjection(proj)
        file2.SetGeoTransform(georef)
        band2 = file2.GetRasterBand(1)
    except:
        print('Impossible de remettre les paramètre du fichier original')
        raise

    # compute the proximity
    try:
        gdal.ComputeProximity(band,band2,["VALUES=1","DISTUNITS=GEO"])
        file2.FlushCache()
    except:
        print('Erreur dans le déroulemnt de la fonction proximity')
        raise

    return output

# Get stats des raster en entrée
def raster_Stats(raster):
    # open raster and choose band to find min, max
    try:
        gtif = gdal.Open(raster)
        srcband = gtif.GetRasterBand(1)
    # Get raster statistics
        stats = srcband.GetStatistics(True, True)
    except:
        print('Erreur avec aquisition statistique')
        raise

    return stats

# Slope calculator
# https://gdal.org/python/
# https://stackoverflow.com/questions/47653271/calculating-aspect-slope-in-python3-x-matlab-gradientm-function
def calculate_slope(DEM):
    try:
        gdal.DEMProcessing(r"D:\dumping_codes\APPSherbrooke\raster\slope.tiff", DEM, 'slope')
    except:
        print('Erreur dans le calcule de la pente')
        raise

# Degrader et reprojeter un Tiff avec gdal.warp 
# https://gdal.org/python/
def reprojectRaster(infile, outfile, epsg, cellsize,extent):
    ds = gdal.Warp(outfile, infile, dstSRS=epsg,
                outputType=gdal.GDT_Float64, xRes=cellsize, yRes=cellsize,ts=extent)
    ds = None
    return outfile

# Crop a raster with a shapefile same as clip
def cropRaster(infile, cropfile, outfile):
    OutTile = gdal.Warp(outfile, 
                    infile,  
                    cutlineDSName=cropfile,
                    cropToCutline=True,
                    dstNodata = 0)

    OutTile = None
    return outfile

# Majority filter
def majorityfilter(input,output):
    wbt = whitebox.WhiteboxTools()
    #print(wbt.list_tools())
    wbt.majority_filter(input,output,filterx=50, 
    filtery=50)
    #whitebox.majority_filter(input,output)

# Exemple how to run the function
# Proximity_Raster(r"D:\dumping_codes\APPSherbrooke\raster\PU.tiff",r"D:\dumping_codes\APPSherbrooke\raster\ProxPU.tiff",1)
# Feature_to_Raster(r'D:\APP_data\parc_industrielAMC.gpkg','GPKG',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster','arbre' + ".tiff"),50,'foret_sherbrooke','age')
# reprojection_Layer(getproj(r'D:\dumping_codes\APPSherbrooke\Ref\DEMZone.tif'),r'D:\dumping_codes\Donnee\Route\routeBuffered_clip.shp','ESRI Shapefile')
# bufferLineAndPoints(r'D:\APP_data\parc_industrielAMC.gpkg',r'D:\dumping_codes\APPSherbrooke\buffer\ruisseau.shp',1,'GOcite_nov2020 Ruisseau')
# reprojectRaster(r'D:\dumping_codes\APPSherbrooke\TestRose\enviro.tiff',r'D:\dumping_codes\APPSherbrooke\TestRose\fuck.tiff','EPSG:32187')
# cropRaster(r'D:\dumping_codes\APPSherbrooke\finalProduct\final.tiff',r'D:\dumping_codes\APPSherbrooke\APP_data\municipSherb.shp',r'D:\dumping_codes\APPSherbrooke\finalProduct\finalCrop.tiff')
# majorityfilter(r'D:\dumping_codes\APPSherbrooke\finalProduct\sociocrop.tiff',r'D:\dumping_codes\APPSherbrooke\finalProduct\finalcropMajority.tiff')
