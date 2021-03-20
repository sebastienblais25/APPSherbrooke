import numpy as np
import os
import random
from osgeo import ogr
from osgeo import gdal, gdal_array
from osgeo import gdalconst


#Rasterize
def Feature_to_Raster(input, type_input, output_tiff, cellsize, layer="", field_name=False, NoData_value=-9999):
    """
    Converts a shapefile into a raster
    """
    # Input
    inp_driver = ogr.GetDriverByName(type_input)
    inp_source = inp_driver.Open(input, 0)
    if layer == "":
        inp_lyr = inp_source.GetLayer()
    else:
        inp_lyr == inp_source.GetLayer(layer)
    inp_srs = inp_lyr.GetSpatialRef()

    # Extent
    x_min, x_max, y_min, y_max = inp_lyr.GetExtent()
    x_ncells = int((x_max - x_min) / cellsize)
    y_ncells = int((y_max - y_min) / cellsize)

    # Output
    out_driver = gdal.GetDriverByName('GTiff')
    if os.path.exists(output_tiff):
        out_driver.Delete(output_tiff)
    out_source = out_driver.Create(output_tiff, x_ncells, y_ncells,
                                   1, gdal.GDT_Int16)

    out_source.SetGeoTransform((x_min, cellsize, 0, y_max, 0, -cellsize))
    out_source.SetProjection(inp_srs.ExportToWkt())
    out_lyr = out_source.GetRasterBand(1)
    out_lyr.SetNoDataValue(NoData_value)

    # Rasterize
    if field_name:
        gdal.RasterizeLayer(out_source, [1], inp_lyr,
                            options=["ATTRIBUTE={0}".format(field_name)])
    else:
        gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[1])

    # Save and/or close the data sources
    inp_source = None
    out_source = None

    # Return
    return output_tiff 

#Reclasify À corriger
def Reclassify_Raster(input,output):
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

    # create new file
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
    file2.GetRasterBand(1).WriteArray(lista)

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache() 

#Raster Calculator for factor
def raster_Calculator(list_input, output, operator):
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
            calc += (i * 0.5)

    # create new file
    file2 = driver.Create(output, file.RasterXSize , file.RasterYSize , 1)
    file2.GetRasterBand(1).WriteArray(calc)

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()

#Raster Calculator for Cirteria
def raster_Calculator_Criteria(list_input, output, operator):
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

    # spatial ref system
    proj = file.GetProjection()
    georef = file.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()
#Proximity

#Change no data to 0
def raster_noData(filenames):
    for fn in filenames:
        ds = gdal.Open(fn, 1)                      # pass 1 to modify the raster
        n = ds.RasterCount                         # get number of bands
        for i in range(1, n+1):
            band = ds.GetRasterBand(i)
            arr = band.ReadAsArray()               # read band as numpy array
            arr = np.where(arr == -6999, 0, arr)  # change 0 to -10000
            band.WriteArray(arr)                   # write the new array
            band.SetNoDataValue(0)            # set the NoData value
            band.FlushCache()                      # save changes
        del ds

#Field Calculator

#Exemple hos to run the function
Feature_to_Raster(r"D:\APP_data\zone_analyse_parcindustriel.shp",'ESRI Shapefile',r'D:\dumping_codes\Tiff\test.tiff',1)