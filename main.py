import numpy
import os
from osgeo import ogr
from osgeo import gdal
from osgeo import gdalconst
## sherbrooke 

driver = ogr.GetDriverByName("ESRI Shapefile")

sr = driver.Open(r"D:\APP_data\zone_analyse_parcindustriel.shp", 0)
raster = gdal.Open(r'D:\dumping_codes\Tiff\test.tif')
print(sr)
print(raster)
lyr = sr.GetLayer("UE")
geot = raster.GetGeoTransform()

# drv_tiff = gdal.GetDriverByName("GTiff") 
# chn_ras_ds = drv_tiff.Create(out_net, raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Float32)
# chn_ras_ds.SetGeoTransform(geot)

# gdal.Rasterize(raster, lyr)

# if ds.RasterCount > 0 and ds.GetLayerCount() > 0:
#     print('Raster and vector')
# elif ds.RasterCount > 0:
#     print('Raster')
# elif ds.GetLayerCount() > 0:
#     print(' vector')
    
