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


time_hydro, frac_hydro = openMixFile('txtFiles/massFrac_hydro_hr.txt')

plt.plot(time_hydro/1.8, frac_hydro, color = 'black', label = 'Hydro-high')

plt.legend(loc = 3, fontsize = 10)
plt.xlim(0, 8)
plt.ylim(0.5, 1.5)
plt.xlabel('Time (tcc)')
plt.ylabel(r'$m( \rho > \rho_{\rm cl}/3)/m_{\rm cl}$')

fig = plt.gcf()
fig.set_size_inches(10, 5)
fig.savefig('MassFrac.pdf')
