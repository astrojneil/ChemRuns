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

outfile = open('runTimes.txt', 'w')
for run in runList:
    outfile.write(run['Name']+', Mach #='+str(run['Mach'])+' Myr \n')
    fileList = os.listdir('../'+run['Name']+'/chkfiles')
    for chk in fileList:
        data = yt.load('../'+run['Name']+'/chkfiles/'+chk)
        timeMyrs = data.current_time.in_units('Myr')
        outfile.write(chk+',\t'+str(timeMyrs)+' \t'+str(timeMyrs/run['tcc'])+' tcc\n')
    outfile.write('\n')
