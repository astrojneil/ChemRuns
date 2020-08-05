#plot the massloss as a function of time
#reads in the mass of the cloud from the global quantities outputting in *.dat

from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

plotName = 'massLoss1_Beta1'

hydro = '../hydro/KH.dat'

time_hydro = FLASHdat_retrieve(hydro, 'time/tcc')
mass_hydro = FLASHdat_retrieve(hydro, 'mass_blob(>rho0/3.)')

#exclude weird values:
exclude = np.where(mass_hydro <= 0.)
mass_hydro = np.delete(mass_hydro, exclude)
time_hydro = np.delete(time_hydro, exclude)

fig, axs = plt.subplots(2, sharex = True)
ax2 = axs[0].twiny()

axs[0].plot(time_hydro, mass_hydro/mass_hydro[0], label = 'H-rad-hr', color = 'black', linewidth = 2)


axs[0].set_xlim(0, 8.)
axs[0].set_ylim(0.5, 1)
axs[1].set_xlim(0, 8.)
axs[1].set_ylim(0.5, 1)
axs[0].legend(loc=3, fontsize = 15)
axs[1].legend(loc=3, fontsize = 15)
axs[0].set_ylabel('Mass Fraction', fontsize = 20)
axs[1].set_ylabel('Mass Fraction', fontsize = 20)
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
