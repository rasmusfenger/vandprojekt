import os
import glob
import subprocess

inFolder = '/Volumes/RASMUS_1/vandprojekt/DEM'
sizePercent = 10

print '\nMosaicking...'
folderList = glob.glob(inFolder + '/DHYM-rain*_TIF_UTM32-ETRS89')
vrtList = []
for folder in folderList:
    head,tail = os.path.split(folder)
    outvrt = os.path.join(inFolder, tail + '.vrt')
    vrtList.append(outvrt)
    if os.path.isfile(outvrt) == False:
        print 'mosaicking ' + folder
        fileList = glob.glob(folder + '/DHYMRAIN_1km_*.tif')
        tempTxt = os.path.join(inFolder, 'buildvrt_filelist.txt')
        with open(tempTxt, 'w') as f1:
            for f in fileList:
                f1.write(f + '\n')
        cmd = ['gdalbuildvrt', '-input_file_list', tempTxt, outvrt]
        subprocess.check_call(cmd)
    else:
        print folder + ' already mosaicked'

print '\nResampling...'
tifList = []
for vrt in vrtList:
    root,ext = os.path.splitext(vrt)
    head,tail = os.path.split(root)
    outTif = os.path.join(inFolder, tail + '_resampled_' + str(sizePercent) + '%.tif')
    tifList.append(outTif)
    if os.path.isfile(outTif) == False:
        print 'resampling ' + outTif
        cmd = ['gdal_translate', '-of', 'GTiff',
               '-outsize', str(sizePercent)+'%', str(sizePercent)+'%',
               vrt, outTif]
        subprocess.check_call(cmd)
    else:
        print outTif + ' already resampled'

print '\nMerging...'
tempTxt = os.path.join(inFolder, 'buildvrt_filelist.txt')
outvrt = os.path.join(inFolder, 'DEM_merge.vrt')
with open(tempTxt, 'w') as f1:
    for tif in tifList:
        f1.write(tif + '\n')
cmd = ['gdalbuildvrt', '-input_file_list', tempTxt, outvrt]
subprocess.check_call(cmd)
os.remove(tempTxt)

print 'finished'
#'-r', 'bilinear'
#'-co', 'TILED=YES'