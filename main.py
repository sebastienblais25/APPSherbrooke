import numpy
import os
from osgeo import ogr
import gdal
## sherbrooke 

driver = ogr.GetDriverByName("OpenFileGDB")
print(driver)
ds = driver.Open(r"D:\APP_data\APP_PI.gdb", 0)

ds.GetLayer("UE")
#<osgeo.ogr.Layer; proxy of <Swig Object of type 'OGRLayerShadow *' at 0x02BB7050> >
print(ds)
sr = ds.GetLayer("UE")
#<osgeo.osr.SpatialReference; proxy of <Swig Object of type 'OSRSpatialReferenceShadow *' at 0x02BB7080> >
sr.ExportToProj4()



#Layer Criteria

# Layer factor


