#plot the mixing fraction for the clouds as a function of time
#reads in files generated with calc_mixfrac.py

import numpy as np
import matplotlib.pyplot as plt

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

time_hydro, frac_hydro = openMixFile('txtFiles/mixFrac_hydro_long.txt')

plt.plot(time_hydro/1.8, frac_hydro, color = 'black', label = 'Hydro-high')

plt.legend(loc = 2)
plt.xlim(0, 8)
plt.ylim(0, 0.35)
plt.xlabel('Time (tcc)')
plt.ylabel('Mixing Fraction')

fig = plt.gcf()
fig.set_size_inches(10, 5)
fig.savefig('MixFrac_noCool_high.pdf')
