#plots the mass fraction of the clouds with time
#reads in files of the calculated mass fractions from calc_massfrac

from openDatFile import FLASHdat_retrieve
import numpy as np
import matplotlib.pyplot as plt

cloudMass =1.223869564736320599e38

def openMixFile(filename):
    mixfile = open(filename, 'r')
    time = []
    fraction = []
    for line in mixfile:
        ls = line.split()
        time.append(float(ls[0]))
        fraction.append(float(ls[1]))

    time = np.array(time)
    fraction = np.array(fraction)
    return time, fraction


#hydro = '/Volumes/GiantDrive2/Blob_paper1/Files/blob_3d_T1e7v1.7e8chi1000.dat'
#hydro_lr = '/Volumes/GiantDrive2/Blob_paper1/Files/blob_3d_T1e7v1.7e8chi1000_lref4.dat'
#time_hydro_ml = FLASHdat_retrieve(hydro, 'time/tcc')
#mass_hydro_ml = FLASHdat_retrieve(hydro, 'mass_blob(>rho0/3.)')

#time_hydro_lr_ml = FLASHdat_retrieve(hydro_lr, 'time/tcc')
#mass_hydro_lr_ml = FLASHdat_retrieve(hydro_lr, 'mass_blob(>rho0/3.)')



time_hydro, frac_hydro = openMixFile('txtFiles/massFrac_hydro_hr.txt')
time_B10_A, frac_B10_A = openMixFile('txtFiles/massFrac_B10A_hr.txt')
time_B10_A_lr, frac_B10_A_lr = openMixFile('txtFiles/massFrac_B10A_lr.txt')
time_hydro_lr, frac_hydro_lr = openMixFile('txtFiles/massFrac_hydro_lr.txt')
time_B10_T, frac_B10_T = openMixFile('txtFiles/massFrac_B10T_hr.txt')
time_B10_T_lr, frac_B10_T_lr = openMixFile('txtFiles/massFrac_B10T_lr.txt')

time_B10_T_nc, frac_B10_T_nc = openMixFile('txtFiles/massFrac_B10T_nc.txt')
time_B10_A_nc, frac_B10_A_nc = openMixFile('txtFiles/massFrac_B10A_nc.txt')
time_hydro_nc, frac_hydro_nc = openMixFile('txtFiles/massFrac_hydro_nc.txt')

plt.plot(time_hydro/1.8, frac_hydro, color = 'black', label = 'Hydro-high')
#plt.plot(time_hydro_lr/1.8, frac_hydro_lr, color = 'black', label = 'Hydro-low', linestyle = 'dashed')
#plt.plot(time_hydro_ml, mass_hydro_ml/cloudMass, color = 'gray', label = 'mass loss hydro')
#plt.plot(time_hydro_lr_ml, mass_hydro_lr_ml/cloudMass, color = 'gray', linestyle = 'dashed', label = 'mass loss hydro lr')


plt.plot(time_B10_A/1.8, frac_B10_A, color = 'red',label = 'M3.5-B10-A-high')
#plt.plot(time_B10_A_lr/1.8, frac_B10_A_lr, color = 'red', label = 'M3.5-B10-A-low', linestyle = 'dashed')

#plt.plot(time_B10_T_lr/1.8, frac_B10_T_lr, color = 'blue',linestyle = 'dashed', label = 'M3.5-B10-T-low')
plt.plot(time_B10_T/1.8, frac_B10_T, color = 'blue', label = 'M3.5-B10-T-high')

plt.plot(time_B10_A_nc/1.8, frac_B10_A_nc, color = 'red', linestyle = 'dotted', label = 'M3.5-B10-A-nc', linewidth = 2)
plt.plot(time_B10_T_nc/1.8, frac_B10_T_nc, color = 'blue', linestyle = 'dotted', label = 'M3.5-B10-T-nc', linewidth = 2)
plt.plot(time_hydro_nc/1.8, frac_hydro_nc, color = 'black', linestyle = 'dotted', label = 'Hydro-nc', linewidth = 2)
#plt.plot([5, 5], [0, 0.35], color = 'red', linestyle = 'dashed')
#plt.annotate('Chk 0048', (4.5, 0.3))
plt.legend(loc = 3, fontsize = 10)
plt.xlim(0, 8)
plt.ylim(0.5, 1.5)
plt.xlabel('Time (tcc)')
plt.ylabel(r'$m( \rho > \rho_{\rm cl}/3)/m_{\rm cl}$')

fig = plt.gcf()
fig.set_size_inches(10, 5)
fig.savefig('MassFrac_noCool_low.pdf')
