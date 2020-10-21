#plot the massloss as a function of time
#reads in the mass of the cloud from the global quantities outputting in *.dat

from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

cloudMass =1.223869564736320599e38

plotName = 'massLoss1v6'

M1 = '../M1-v480-T1-chem/runfiles/CT.dat'
M6 = '../M6.2-v3000-T1-chem/runfiles/CT.dat'
M3 = '../M3.6-v3000-T3-chem/runfiles/CT.dat'

time_M1 = FLASHdat_retrieve(M1, 'time/tcc')
mass_M1 = FLASHdat_retrieve(M1, 'mass_blob(>rho0/3.)')

time_M6 = FLASHdat_retrieve(M6, 'time/tcc')
mass_M6 = FLASHdat_retrieve(M6, 'mass_blob(>rho0/3.)')

time_M3 = FLASHdat_retrieve(M3, 'time/tcc')
mass_M3 = FLASHdat_retrieve(M3, 'mass_blob(>rho0/3.)')

#exclude weird values:
#exclude = np.where(mass_hydro <= 0.)
#mass_hydro = np.delete(mass_hydro, exclude)
#time_hydro = np.delete(time_hydro, exclude)

fig, axs = plt.subplots(2, sharex=True)
ax2 = axs[0].twiny()

print(M6[0:6])

axs[0].plot(time_M6, mass_M6/cloudMass, label = 'M6.2-v3000-T1', color = 'black', linewidth = 2)
axs[0].plot(time_M1, mass_M1/cloudMass, label = 'M1-v480-T1', color = 'red', linewidth = 2)
axs[0].plot(time_M3, mass_M3/cloudMass, label = 'M3.6-v3000-T3', color = 'orange', linewidth = 2)


axs[0].set_xlim(0, 8.)
axs[0].set_ylim(0.5, 1)
#axs[1].set_xlim(0, 8.)
#axs[1].set_ylim(0.5, 1)
axs[0].legend(loc=3, fontsize = 15)
#axs[1].legend(loc=3, fontsize = 15)
axs[0].set_ylabel('Mass Fraction', fontsize = 20)
#axs[1].set_ylabel('Mass Fraction', fontsize = 20)
axs[1].set_xlabel(r'Time ($t_{\rm cc}$)', fontsize = 20)

ax1X = axs[0].get_xticks()
ax2X = []
for X in ax1X:
	ax2X.append(X*1.8)

ax2.set_xticks(ax1X[1:])
ax2.set_xbound(axs[0].get_xbound())
ax2.set_xticklabels(ax2X[1:])
ax2.set_xlabel(r'Time (Myrs)', fontsize = 20)

fig.subplots_adjust(top=0.85)
fig.set_size_inches(10, 9)
plt.tight_layout()

fig.savefig(plotName+'.pdf')
