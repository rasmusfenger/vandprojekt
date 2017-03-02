# reproject each of polarisations (gdal_warp, EPSG: ?, LZW compression, res 10m, nearest
# composit with gdalbuildvrt

import glob
import os
import subprocess

inPath = '/Volumes/RASMUS_1/vandprojekt/sentinel1/original'
imgFolder = 'S1A_IW_GRDH_1SDV_20151221T054031_20151221T054056_009136_00D23F_C69E.SAFE'
outFolder = '/Volumes/RASMUS_1/vandprojekt/sentinel1/processed'
epsg = 25832
outRes = 10

inFiles = glob.glob(os.path.join(inPath,imgFolder) + '/measurement/s1*.tiff')
print 'Reprojecting...'
tifList = []
for inFile in inFiles:
    root,ext = os.path.splitext(inFile)
    head,tail = os.path.split(root)
    outFile = os.path.join(outFolder, 'reprojected', tail + '_reproj.tif')
    tifList.append(outFile)
    if os.path.isfile(outFile) == False:
        cmd = ['gdalwarp',
               '-s_srs','EPSG:4326',
               '-t_srs', 'EPSG:'+str(epsg),
               '-tr', str(outRes), str(outRes),
               '-ot', 'Int16',
               '-r', 'near',
               inFile, outFile]
        subprocess.check_call(cmd)
    else:
        print inFile + ' already reprojected'

print '\nCompositing...'
tempTxt = os.path.join(outFolder, 'buildvrt_filelist.txt')
outvrt = os.path.join(outFolder, imgFolder[:-5] + '.vrt')
with open(tempTxt, 'w') as f1:
    for tif in tifList:
        f1.write(tif + '\n')
cmd = ['gdalbuildvrt',
       '-separate',
       '-input_file_list', tempTxt, outvrt]
subprocess.check_call(cmd)
os.remove(tempTxt)
print 'finished'

'''
ds = gdal.Open(inFiles[0], gdal.GA_ReadOnly)
drv = gdal.GetDriverByName('GTiff')
outTif = drv.Create(outFile, ds.RasterXSize, ds.RasterYSize, 2, gdal.GDT_UInt16)

b = 1
for inFile in inFiles:
    ds = gdal.Open(inFiles[0], gdal.GA_ReadOnly)
    band = ds.GetRasterBand(1)
    array = band.ReadAsArray()
    outTif.GetRasterBand(b).WriteArray(array)
    b = b + 1
    outTif.SetGeoTransform(ds.GetGeoTransform())
outTif.SetGCPs(ds.GetGCPs(), ds.GetGCPProjection())
array = None
outTif = None
'''