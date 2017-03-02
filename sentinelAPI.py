import subprocess

cmd = ['sentinel search',
       '-s', '20170101',
       'rasmusfenger', 'Gubbi2084',
       '/Volumes/RASMUS_1/vandprojekt/test/fyn1.geojson']
print cmd
subprocess.check_call(cmd)


#cmd = ["sentinel search",
#       '-s', '20140401',
#       '-e', '20141231',
#       '-q', 'producttype=GRD, sensoroperationalmode=IW, orbitdirection=Ascending',
#       '-f',
#       '-p', '/Volumes/RASMUS_1/vandprojekt/download',
#       'rasmusfenger', 'Gubbi2084',
#       '/Volumes/RASMUS_1/vandprojekt/test/fyn1.geojson']