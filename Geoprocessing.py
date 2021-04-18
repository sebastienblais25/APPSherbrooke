import numpy as np
import os
import random
import shutil
from osgeo import ogr
from osgeo import osr
from osgeo import gdal, gdal_array
from osgeo import gdalconst

projection = osr.SpatialReference(wkt = r'PROJCS["NAD83 / MTM zone 7",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-70.5],PARAMETER["scale_factor",0.9999],PARAMETER["false_easting",304800],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["E(X)",EAST],AXIS["N(Y)",NORTH],AUTHORITY["EPSG","32187"]]')


# Setup les dossiers pour que le programmes fonctionne comme il le faut
def setUpDirectory(path):
    # Check if the folder of source layer
    if not os.path.exists(os.path.join(path,'source')):
        print('add the source folder for the multicriteria analysis')
    # Create folder for the raster
    if os.path.exists(os.path.join(path,'raster')):
        shutil.rmtree(os.path.join(path,'raster'))
    os.mkdir(os.path.join(path,'raster'))
    # Create folder for the raster
    if os.path.exists(os.path.join(path,'proximity')):
        shutil.rmtree(os.path.join(path,'proximity'))
    os.mkdir(os.path.join(path,'proximity'))
    # Create folder for the finalProduct
    if os.path.exists(os.path.join(path,'finalProduct')):
        shutil.rmtree(os.path.join(path,'finalProduct'))
    os.mkdir(os.path.join(path,'finalProduct'))
    # Create folder for the reproject
    if os.path.exists(os.path.join(path,'reproject')):
        shutil.rmtree(os.path.join(path,'reproject'))
    os.mkdir(os.path.join(path,'reproject'))
    # Create folder for the reclassify
    if os.path.exists(os.path.join(path,'reclassify')):
        shutil.rmtree(os.path.join(path,'reclassify'))
    os.mkdir(os.path.join(path,'reclassify'))

# Clean tous les dossier pour prendre l moins d'espace possible
def cleanUpDirectory(path):
    # Delete Folder
    shutil.rmtree(os.path.join(path,'raster'))
    shutil.rmtree(os.path.join(path,'proximity'))
    shutil.rmtree(os.path.join(path,'reproject'))   

# Permet de mettre un petit buffer autour des objet qui ne sont pas des polygones pour réaliser un rasterize
def bufferLineAndPoints(inputfn, outputBufferfn, bufferDist,layername):
    inputds = ogr.Open(inputfn)
    inputlyr = inputds.GetLayer(layername)

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)
    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in inputlyr:
        ingeom = feature.GetGeometryRef()
        geomBuffer = ingeom.Buffer(bufferDist)

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geomBuffer)
        bufferlyr.CreateFeature(outFeature)


    bufferlyr.SetProjection(inp_lyr.GetSpatialRef().ExportToWkt())

    ds = None
    return outputBufferfn

# Donne l'extent de référence
def getExtent(input):
    # Chercher le driver pour la lecture
    inp_driver = ogr.GetDriverByName(type_input)
    # Lecture du fichier
    inp_source = inp_driver.Open(input, 0)
    # Si un nom de couche n'est pas donner on va chercher la premiere couche sinon on prendre celle avec le nnom
    if layer == "":
        inp_lyr = inp_source.GetLayer()
    else:
        inp_lyr = inp_source.GetLayer(layer)
    # On va chercher les références spatiales de la couches
    return inp_lyr.GetExtent()

# Donne la référence spatiale de référence
def getproj(input):
    # #shapefile with the from projection
    driver = ogr.GetDriverByName(typefile)
    dataSource = driver.Open(input, 0)
    if layer == "":
        inp_lyr = dataSource.GetLayer()
    else:
        inp_lyr = dataSource.GetLayer(layer)
    # inp_lyr = openVectorFile(input, typefile, layer)
    output = input
    #set spatial reference and transformation
    sourceprj = inp_lyr.GetSpatialRef()
    return sourceprj

# Reprojection des couches à utiliser
def reprojection_Layer(input, typefile, layer=""):

    # #shapefile with the from projection
    driver = ogr.GetDriverByName(typefile)
    dataSource = driver.Open(input, 0)
    if layer == "":
        inp_lyr = dataSource.GetLayer()
    else:
        inp_lyr = dataSource.GetLayer(layer)
    # inp_lyr = openVectorFile(input, typefile, layer)
    output = input
    #set spatial reference and transformation
    sourceprj = inp_lyr.GetSpatialRef()
    
    if sourceprj != projection:
        if layer == "":
            output = os.path.join(r"D:\dumping_codes\APPSherbrooke\reproject", input.split("\\")[-1])
        else: 
            output = os.path.join(r"D:\dumping_codes\APPSherbrooke\reproject", layer + '.shp')
        transform = osr.CoordinateTransformation(sourceprj, projection)
        
        to_fill = ogr.GetDriverByName("Esri Shapefile")
        ds = to_fill.CreateDataSource(output)
        outlayer = ds.CreateLayer('', projection, ogr.wkbPolygon)
        #outlayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        fields = [field.name for field in inp_lyr.schema]
        for i in fields:
            outlayer.CreateField(ogr.FieldDefn(i, ogr.OFTString))

        #apply transformation
        i = 0

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
                    print('Special Character')
            feat.SetGeometry(geom)
            outlayer.CreateFeature(feat)
            i += 1
            feat = None
        # changer parametre path pour le nouveau chemin

    ds = None
    return output

# Fonction pour effectuer un rasterize sur les fichiers vectorielle
def Feature_to_Raster(input, type_input, output_tiff, cellsize, layer="", burnvalue=False, field_name=False, NoData_value=0):
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
        raise Exception('Impossible to read the layer')
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
    

    # Rasterize
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

    # Returne le nom du fichier 
    return output_tiff 

# Reclassify À corriger
def Reclassify_Raster(input,output, maskin,table):
    driver = gdal.GetDriverByName('GTiff')
    file = gdal.Open(input)
    band = file.GetRasterBand(1)
    lista = band.ReadAsArray()

    mask= gdal.Open(maskin)
    bandmask = mask.GetRasterBand(1)
    listMask = bandmask.ReadAsArray()
    reclassif = table.split(';')

    # reclassification
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
            else:
                lista[i,j] = -1

    # Création d'un nouveau fichier pour la nouvelle reclassification
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float32'))
    # Ajout de la matrice dans le fichier
    file2.GetRasterBand(1).WriteArray(lista)

    # remet les paramèetre du fichier original
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()

    return output

# Raster Calculator pour les critère
def raster_Calculator(list_input, output):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    # Ouvre tous les fichiers a lire
    for i in list_input:
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

    return output

# Raster Calculator pour les facteur a travailler
def raster_Calculator_factor(list_input, output):
    driver = gdal.GetDriverByName('GTiff')
    list_array = []
    for i in list_input:
        file = gdal.Open(i.rasPath)
        band = file.GetRasterBand(1)
        list_array.append(band.ReadAsArray())

    for idx, i in enumerate(list_array):
        if idx == 0 :
            calc = (i * float(list_input[idx].weight))
        else:
            calc += (i * float(list_input[idx].weight))

    # create new file
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1, gdal.GetDataTypeByName('Float32'))
    file2.GetRasterBand(1).WriteArray(calc)
    file2.GetRasterBand(1).SetNoDataValue(0)

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()
    return output

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

    return output

# Get stats des raster en entrée
def raster_Stats(raster):
    # open raster and choose band to find min, max
    gtif = gdal.Open(raster)
    srcband = gtif.GetRasterBand(1)
    # Get raster statistics
    stats = srcband.GetStatistics(True, True)
    return stats

# Slope calculator
# https://gdal.org/python/
# https://stackoverflow.com/questions/47653271/calculating-aspect-slope-in-python3-x-matlab-gradientm-function
def calculate_slope(DEM):
    gdal.DEMProcessing(r"D:\dumping_codes\APPSherbrooke\raster\slope.tiff", DEM, 'slope')

# Degrader et reprojeter un Tiff avec gdal.warp 
# https://gdal.org/python/

# Field Calculator

# Exemple hos to run the function
# Proximity_Raster(r"D:\dumping_codes\APPSherbrooke\raster\PU.tiff",r"D:\dumping_codes\APPSherbrooke\raster\ProxPU.tiff",1)
Feature_to_Raster(r'D:\APP_data\parc_industrielAMC.gpkg','GPKG',os.path.join(r'D:\dumping_codes\APPSherbrooke\raster','arbre' + ".tiff"),50,'foret_sherbrooke','age')
# reprojection_Layer(r'D:\APP_data\parc_industrielAMC.gpkg','GPKG','GOcite_nov2020 Riviere')
# bufferLineAndPoints(r'D:\APP_data\parc_industrielAMC.gpkg',r'D:\dumping_codes\APPSherbrooke\buffer\ruisseau.shp',1,'GOcite_nov2020 Ruisseau')