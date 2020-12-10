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

from yt.funcs import mylog
mylog.setLevel(50) # This sets the log level to "CRITICAL"

kpc = 3.086e+21*centimeter
c_speed = 3.0e10  #cm/s
mp = 1.6726e-24*gram #grams
kb = 1.3806e-16*erg/Kelvin   #egs/K

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

#function to read in spectrum, convert to velocity and return
#wavelength and flux numpy arrays
def convert_to_vel(filename, rest_wave):
    #load spectrum; will need to add a case when this is a txt file rather than h5
    wavelength = []
    flux = []
    f = open(filename, 'r')
    i = 1
    for line in f:
        if i > 3:
            splitline = line.split()
            wavelength.append(float(splitline[0]))
            flux.append(float(splitline[1]))
        i=i+1

    wavelength = np.array(wavelength)
    flux = np.array(flux)
    vel = c_speed*(wavelength/rest_wave -1)
    #returns with velocities in cm/s
    return vel, flux


#function to determine the velocity of the cloud for a particular run
#will return an array of velocities (km/s) for the appropriate velocity bins to use
#in the observational data.
def findCloudVel(runName, f_list):
    velList = []
    velFrames = []
    for i in f_list:
        data = yt.load('../'+runName+'/chkfiles/CT_hdf5_chk_'+i)
        allDataRegion = data.all_data()
        cloudRegion = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])  #at or above 1/3 original density (1e-24)
        avg_vy_cloud = cloudRegion.quantities.weighted_average_quantity('vely', 'ones') #vely is the velocity in the radial direction (towards/away obs)

        #need to add the frame velocity!
        #get the frame velocity
        f = h5py.File('../'+runName+'/chkfiles/CT_hdf5_chk_'+i, 'r')
        velframe = f['real scalars'][7][1] #cm/s
        velFrames.append(velframe/1.0e5) #append frame vel in km/s
        f.close()

        vy_cloud = (avg_vy_cloud.value+velframe)/1.0e5  #convert to km/s
        velList.append(vy_cloud)

    print('Frame vels:')
    print(velFrames)
    print('Cloud vels:')
    print(velList)
    return velList, velFrames


#calculate the column densities
def getDensities(runName, time, ionList, velBin, frameVel):
    frameVel = frameVel*1.0e5*(centimeter/second)
    data = yt.load('../'+runName+'/chkfiles/CT_hdf5_chk_'+time)
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun', sampling_type = 'cell')

    bList = []
    vList = []
    TList = []

    for ion in ionList:
        print(ion['name'], end = ' ')

        for source in ['chem']:  #here you can define chem or trident
            #add the ion to the dataset
            _ = addfield(data, ion['atom'], ion['ion'], 'dens', source)

            #select the region
            reg = data.all_data()

            p = data.proj(ion[source], 1)

            frb = yt.FixedResolutionBuffer(p, (-2.464e21, 2.464e21, -2.464e21, 2.464e21), (800, 800))

            #flatten the frb to a 1d array
            flattened_num = frb[ion[source]].flatten()
            projectedNum = flattened_num

            #rank sort the projected taus and then make plot
            sorted_num = np.sort(projectedNum, kind='quicksort')

            #find the average velocity for the ion
            average_vely = reg.quantities.weighted_average_quantity('vely', ion[source])+frameVel

            average_temp = reg.quantities.weighted_average_quantity('temperature', ion[source])

            #write out the ranked Column densities to be used to make a fit
            writeFile = open('../rankNum'+ion['ionfolder']+'rankNum'+runName+'_v'+str(velBin)+'.txt', 'w')
            for i in range(len(sorted_num)):
                writeString = str(sorted_num[i].value)+'\n'
                writeFile.write(writeString)
            writeFile.close()

            #add b^2 thermal as a field
            def _btherm(field, data):
                topFrac = 2.0*kb*data['temperature']
                botFrac = ion['massNum']*mp
                b = topFrac/botFrac
                return b

            data.add_field(('gas', 'b_therm'), function=_btherm, display_name="B thermal squared", units = 'cm**2/s**2', force_override=True, sampling_type = 'cell')
            #project b thermal
            btherm = data.proj('b_therm', 1, weight_field=ion[source])
            frb_therm = yt.FixedResolutionBuffer(btherm, (-2.464e21, 2.464e21, -2.464e21, 2.464e21), (800, 800))
            flattened_btherm = frb_therm['b_therm'].flatten()

            #add b^2 doppler as a field
            def _bdop(field, data):
                b = (data['vely'] - average_vely)**2
                return b  #multiply by number density to weight the b value

            data.add_field(('gas', 'b_doppler'), function=_bdop, display_name="B doppler squared", units = 'cm**2/s**2', force_override=True, sampling_type = 'cell')
            #project b doppler
            bdop = data.proj('b_doppler', 1, weight_field=ion[source])
            frb_dop = yt.FixedResolutionBuffer(bdop, (-2.464e21, 2.464e21, -2.464e21, 2.464e21), (800, 800))
            flattened_bdop = frb_dop['b_doppler'].flatten()

            good_btherm = flattened_btherm[~np.isnan(flattened_btherm)]
            good_bdop = flattened_bdop[~np.isnan(flattened_bdop)]

            #add the two b's and sqrt
            b_tot_Sq = good_btherm+good_bdop

            b_tot = np.sqrt(b_tot_Sq)

            #compute the average of the summation of b projections
            b_avg = np.average(b_tot)

            bList.append(b_avg)
            vList.append(average_vely)
            TList.append(average_temp)
            #print(b_avg)
            #print(average_vely)


    return bList, vList, TList



def main():
    #define the runs and ions
    run1 = {'Name':'M1-v480-T1-chem',
        'times': ['0000', '0030', '0041']}
    run2 = {'Name':'M6.2-v3000-T1-chem',
        'times':['0000', '0076']}
    run3 = {'Name':'M3.6-v3000-T3-chem',
        'times':['0000', '0031']}
    runList = []
    runList.append(run1)
    runList.append(run2)
    runList.append(run3)


    ion1 = {'atom':'H',
        'ion':'I',
        'name':'HI',
        'chem': 'densHI_chem',
        'tri': 'densHI_tri',
        'ionfolder':'/HI/',
        'rest_wave': 1215.67,
            'data_file': '../Files/S1226-o6-forJNeil',
            'sigma': 4.3394e-18,
            'massNum': 1.0}
    ion2 = {'atom':'Mg',
        'ion':'II',
        'name':'MgII',
        'chem': 'densMgII_chem',
        'tri': 'densMgII_tri',
        'ionfolder':'/MgII/',
        'rest_wave': 1239.92,
            'data_file': '../Files/S1226-o6-forJNeil',
            'sigma': 6.60717e-21,
            'massNum': 24.3050}
    ion3 = {'atom':'C',
        'ion':'III',
        'name':'CIII',
        'chem': 'densCIII_chem',
        'tri': 'densCIII_tri',
        'ionfolder':'/CIII/',
        'rest_wave': 977.02,
            'data_file': '../Files/S1226-o6-forJNeil',
            'sigma': 6.359e-18,
            'massNum': 12.0107}
    ion4 = {'atom':'C',
        'ion':'IV',
        'name':'CIV',
        'chem': 'densCIV_chem',
        'tri': 'densCIV_tri',
        'ionfolder':'/CIV/',
        'rest_wave': 1548.18,
        'data_file': '../Files/S1226-redward-forJNeil',
        'sigma': 2.5347e-18,
        'massNum': 12.0107}
    ion5 = {'atom':'N',
        'ion':'V',
        'name':'NV',
        'chem': 'densNV_chem',
        'tri': 'densNV_tri',
        'ionfolder':'/NV/',
        'rest_wave': 1242.8,
        'data_file': '../Files/S1226-redward-forJNeil',
        'sigma': 8.3181e-19,   #UM. is it actually e-19?   -12/7/17
        'massNum': 14.0067}
    ion6 = {'atom':'O',
        'ion':'VI',
        'name':'OVI',
        'chem': 'densOVI_chem',
        'tri': 'densOVI_tri',
        'ionfolder':'/OVI/',
        'rest_wave': 1031.91,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 1.1776e-18,
        'massNum': 15.9994}
    ion7 = {'atom':'Ne',
        'ion':'VIII',
        'name':'NeVIII',
        'chem': 'densNeVIII_chem',
        'tri': 'densNeVIII_tri',
        'ionfolder':'/NeVIII/',
        'rest_wave': 770.406,
            'data_file': '../Files/S1226-o6-forJNeil',
            'sigma': 6.74298e-19,
            'massNum': 20.1797}


    ionList = []
    ionList.append(ion1)
    ionList.append(ion2)
    ionList.append(ion3)
    ionList.append(ion4)
    ionList.append(ion5)
    ionList.append(ion6)
    ionList.append(ion7)

    writebv_file = open('../rankNum/Totalrun_allIon_bv_temp.txt', 'w')
    writebv_file.write('Run, frame, Ion, Average_vel(cm/s), b(cm/s), T(K)\n')
    for run in runList:
        print('Beginning run {}'.format(run['Name']))
        print('Calculating frame velocities...')
        velBins, velFrames = findCloudVel(run['Name'], run['times']) #velocities in km/s

        print('Looping through times...')
        for t in range(len(velBins)):
            print("\nTime {}:".format(t))
            #this function outputs the ranked num files
            bList, vList, TList = getDensities(run['Name'], run['times'][t], ionList, t, velFrames[t])

            for i in range(len(ionList)):
                writeString = run['Name']+', '+str(t)+', '+ionList[i]['ionfolder'][1:-1]+', '+str(vList[i].value)+', '+str(bList[i])+', '+str(TList[i])+'\n'
                #print(writeString)
                writebv_file.write(writeString)

    writebv_file.close()


if __name__ =="__main__":
    main()
