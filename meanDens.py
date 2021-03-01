import yt
import numpy as np
import os

run1 = {'Name':'M1-v480-T1-chem', 'Mach':1, 'tcc':6.4}
run2 = {'Name':'M6.2-v3000-T1-chem', 'Mach':6.2, 'tcc':1.0}
run3 = {'Name':'M3.6-v3000-T3-chem', 'Mach':3.6, 'tcc':1.8}

runList = []
runList.append(run1)
runList.append(run2)
runList.append(run3)

for run in runList:
    outfile = open(run['Name']+'_meanDens.txt', 'w')
    outfile.write('Time,meanDens\n')
    fileList = os.listdir('../'+run['Name']+'/chkfiles')
    for chk in fileList:
        data = yt.load('../'+run['Name']+'/chkfiles/'+chk)
        dataRegion = data.all_data()
        cloud_region1 = dataRegion.cut_region(['obj["blob"] > 0.'])
        mean_dens = cloud_region1.quantities.weighted_average_quantity("density", "ones")
        time = data.current_time.in_units('Myr')/run['tcc']

        outfile.write(str(time)+', \t'+str(mean_dens)+'\n')
    outfile.close()
