#script to pull out the list of column densities within the center of the simulations
#centered on the cloud. These are then written to a file to be used to
#calculate the cumulative distribution of the column densities

import yt
import numpy as np
import trident as tri
import h5py
from massFracs import *
import pandas as pd
from yt.units import centimeter, gram, second, Kelvin, erg

kpc = 3.086e+21*centimeter
c_speed = 3.0e10  #cm/s
mp = 1.6726e-24*gram #grams
kb = 1.3806e-16*erg/Kelvin   #egs/K

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

#calculate the column densities
def getDensities(runName, time, ionList, t, unRank_chem, unRank_tri):
    data = yt.load('../'+runName+'/chkfiles/CT_hdf5_chk_'+time)
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

    for ion in ionList:

        for source in ['chem', 'tri']:
            #add the ion to the dataset
            _ = addfield(data, ion['atom'], ion['ion'], 'dens', source)

            p = data.proj(ion[source], 1)

            frb = yt.FixedResolutionBuffer(p, (-2.464e21, 2.464e21, -2.464e21, 2.464e21), (800, 800))

            #flatten the frb to a 1d array
            flattened_num = frb[ion[source]].flatten()
            projectedNum = flattened_num

            #save to the database
            if source == 'chem':
                unRank_chem[ion['name']+'_'+str(t)] = projectedNum
            else:
                unRank_tri[ion['name']+'_'+str(t)] = projectedNum

    return



def main():
    #define the runs and ions
    run1 = {'Name':'M1-v480-T1-chem',
        'times': ['0000', '0044']}
    run2 = {'Name':'M6.2-v3000-T1-chem',
        'times':['0000', '0032']}
    run3 = {'Name':'M3.6-v3000-T3-chem',
        'times':['0000']}
    runList = []
    runList.append(run1)
    runList.append(run2)


    ion1 = {'atom':'H',
        'ion':'I',
        'name':'HI',
        'chem': 'densHI_chem',
        'tri': 'densHI_tri'}
    ion2 = {'atom':'Mg',
        'ion':'II',
        'name':'MgII',
        'chem': 'densMgII_chem',
        'tri': 'densMgII_tri'}
    ion3 = {'atom':'C',
        'ion':'III',
        'name':'CIII',
        'chem': 'densCIII_chem',
        'tri': 'densCIII_tri'}
    ion4 = {'atom':'C',
        'ion':'IV',
        'name':'CIV',
        'chem': 'densCIV_chem',
        'tri': 'densCIV_tri'}
    ion5 = {'atom':'N',
        'ion':'V',
        'name':'NV',
        'chem': 'densNV_chem',
        'tri': 'densNV_tri'}
    ion6 = {'atom':'O',
        'ion':'VI',
        'name':'OVI',
        'chem': 'densOVI_chem',
        'tri': 'densOVI_tri'}
    ion7 = {'atom':'Ne',
        'ion':'VIII',
        'name':'NeVIII',
        'chem': 'densNeVIII_chem',
        'tri': 'densNeVIII_tri'}


    ionList = []
    ionList.append(ion1)
    ionList.append(ion2)
    ionList.append(ion3)
    ionList.append(ion4)
    ionList.append(ion5)
    ionList.append(ion6)
    ionList.append(ion7)

    for run in runList:
        unRank_chem = pd.DataFrame()
        unRank_tri = pd.DataFrame()

        for t in [0, 1]:
            getDensities(run['Name'], run['times'][t], ionList, t, unRank_chem, unRank_tri)

        unRank_chem.to_csv('../'+run['Name']+'/'+run['Name']+'_coldens_chem.csv')
        unRank_tri.to_csv('../'+run['Name']+'/'+run['Name']+'_coldens_tri.csv')

if __name__ =="__main__":
    main()
