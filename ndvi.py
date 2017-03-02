inFile = '/Volumes/RASMUS_1/vandprojekt/sentinel2/S2A_USER_MTD_SAFL2A_PDMC_20160724T182306_R108_V20160724T103229_20160724T103229_10m_UTM32N.tif'
outFile = '/Volumes/RASMUS_1/vandprojekt/sentinel2/20160724_ndvi.tif'

import gdal
import numpy as np

ds = gdal.Open(inFile, gdal.GA_ReadOnly)

bandRed = ds.GetRasterBand(3)
aRed = bandRed.ReadAsArray().astype(np.float32)

bandNir = ds.GetRasterBand(4)
aNir = bandNir.ReadAsArray().astype(np.float32)

ndvi = (aNir - aRed) / (aNir + aRed + 0.0000001)

# save to output tif
drv = gdal.GetDriverByName('GTiff')
outTif = drv.Create(outFile, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
outTif.SetGeoTransform(ds.GetGeoTransform())
outTif.SetProjection(ds.GetProjection())
outTif.GetRasterBand(1).WriteArray(ndvi)
outTif = None

print 'finished'