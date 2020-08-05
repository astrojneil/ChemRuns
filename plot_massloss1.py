#plot the massloss as a function of time
#reads in the mass of the cloud from the global quantities outputting in *.dat

from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)

hydro = '/Volumes/GiantDrive2/Blob_paper1/Files/blob_3d_T1e7v1.7e8chi1000.dat'
hydro_lr = '/Volumes/GiantDrive2/Blob_paper1/Files/blob_3d_T1e7v1.7e8chi1000_lref4.dat'
#b100_a = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B100_A/KH.dat'
b10_a = '/Volumes/GiantDrive2/MHD_overflow//M3.5_B10_A_highres/KH.dat'
#b100_t = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B100_T/KH.dat'
b10_t = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B10_T_highres/KH.dat'
#M3.5: = '../Blob_paper1/Files/blob_3d_T1e7v1.7e8chi1000.dat'
#M6.5: = '../Blob_paper1/Files/blob_3d_T3e6v1.7e8chi300.dat'
b10_a_lr = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B10_A_lowres/KH.dat'
b10_t_lr = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B10_T_lowres/KH_final.dat'

b10_t_nc = '/Volumes/GiantDrive2/MHD_overflow/B10_T_noCool_highres/KH_copy.dat'
b10_a_nc = '/Volumes/GiantDrive2/MHD_overflow/B10_A_noCool_highres/KH_copy.dat'
hydro_nc = '/Volumes/GiantDrive2/MHD_overflow/Hydro_noCool/KH.dat'

b1_t = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B1_T/extraChk/KH_copy.dat'
b1_a = '/Volumes/GiantDrive2/MHD_overflow/M3.5_B1_A/KH_copy_test.dat'

plotName = 'massLoss1_Beta1'

#time_hydro_old = FLASHdat_retrieve(hydro_old, 'time/tcc')
#mass_hydro_old = FLASHdat_retrieve(hydro_old, 'mass_blob(>rho0/3.)')

time_hydro = FLASHdat_retrieve(hydro, 'time/tcc')
mass_hydro = FLASHdat_retrieve(hydro, 'mass_blob(>rho0/3.)')
time_hydro_lr = FLASHdat_retrieve(hydro_lr, 'time/tcc')
mass_hydro_lr = FLASHdat_retrieve(hydro_lr, 'mass_blob(>rho0/3.)')
time_hydro_nc = FLASHdat_retrieve(hydro_nc, 'time/tcc')
mass_hydro_nc = FLASHdat_retrieve(hydro_nc, 'mass_blob(>rho0/3.)')

time_b10_a = FLASHdat_retrieve(b10_a, 'time/tcc')
mass_b10_a = FLASHdat_retrieve(b10_a, 'mass_blob(>rho0/3.)')
time_b10_a_lr = FLASHdat_retrieve(b10_a_lr, 'time/tcc')
mass_b10_a_lr = FLASHdat_retrieve(b10_a_lr, 'mass_blob(>rho0/3.)')
time_b10_a_nc = FLASHdat_retrieve(b10_a_nc, 'time/tcc')
mass_b10_a_nc = FLASHdat_retrieve(b10_a_nc, 'mass_blob(>rho0/3.)')

time_b10_t = FLASHdat_retrieve(b10_t, 'time/tcc')
mass_b10_t = FLASHdat_retrieve(b10_t, 'mass_blob(>rho0/3.)')
time_b10_t_lr = FLASHdat_retrieve(b10_t_lr, 'time/tcc')
mass_b10_t_lr = FLASHdat_retrieve(b10_t_lr, 'mass_blob(>rho0/3.)')
time_b10_t_nc = FLASHdat_retrieve(b10_t_nc, 'time/tcc')
mass_b10_t_nc = FLASHdat_retrieve(b10_t_nc, 'mass_blob(>rho0/3.)')

time_b1_t = FLASHdat_retrieve(b1_t, 'time/tcc')
mass_b1_t = FLASHdat_retrieve(b1_t, 'mass_blob(>rho0/3.)')

time_b1_a = FLASHdat_retrieve(b1_a, 'time/tcc')
mass_b1_a = FLASHdat_retrieve(b1_a, 'mass_blob(>rho0/3.)')


#exclude weird values:
exclude = np.where(mass_hydro <= 0.)
mass_hydro = np.delete(mass_hydro, exclude)
time_hydro = np.delete(time_hydro, exclude)

#exclude weird values:
exclude = np.where(mass_b10_a <= 0.)
mass_b10_a = np.delete(mass_b10_a, exclude)
time_b10_a = np.delete(time_b10_a, exclude)


fig, axs = plt.subplots(2, sharex = True)
ax2 = axs[0].twiny()

axs[0].plot(time_hydro, mass_hydro/mass_hydro[0], label = 'H-rad-hr', color = 'black', linewidth = 2)
#plt.plot(time_hydro_lr, mass_hydro_lr/mass_hydro_lr[0], label='Hydro-low', color = 'black', linestyle = 'dashed')
axs[0].plot(time_hydro_nc, mass_hydro_nc/mass_hydro_nc[0], label = 'H-nonrad-hr', color = 'black', linestyle = 'dashed', linewidth=2)

axs[1].plot(time_hydro, mass_hydro/mass_hydro[0], label = 'H-rad-hr', color = 'black', linewidth = 2)
#plt.plot(time_hydro_lr, mass_hydro_lr/mass_hydro_lr[0], label='Hydro-low', color = 'black', linestyle = 'dashed')
axs[1].plot(time_hydro_nc, mass_hydro_nc/mass_hydro_nc[0], label = 'H-nonrad-hr', color = 'black', linestyle = 'dashed', linewidth=2)


axs[0].plot(time_b10_a, mass_b10_a/mass_b10_a[0], label='A-rad-hr', color = 'red', linewidth=2)
axs[0].plot(time_b1_a, mass_b1_a/mass_b1_a[0], label = 'A-B1-rad-hr', color = 'red', linewidth=4, linestyle = 'dotted')
#plt.plot(time_b10_a_lr, mass_b10_a_lr/mass_b10_a_lr[0], label='M3.5-B10-A-low', color = 'red', linestyle = 'dashed')
axs[0].plot(time_b10_a_nc, mass_b10_a_nc/mass_b10_a_nc[0], label = 'A-nonrad-hr', color = 'red', linestyle = 'dashed', linewidth=2)

axs[1].plot(time_b10_t, mass_b10_t/mass_b10_t[0], label='T-rad-hr', color = 'blue', linewidth=2)
axs[1].plot(time_b1_t, mass_b1_t/mass_b1_t[0], label = 'T-B1-rad-hr', color = 'blue', linewidth=4, linestyle = 'dotted')
#plt.plot(time_b10_t_lr, mass_b10_t_lr/mass_b10_t_lr[0], label='M3.5-B10-T-low', color = 'blue', linestyle = 'dashed')
axs[1].plot(time_b10_t_nc, mass_b10_t_nc/mass_b10_t_nc[0], label = 'T-nonrad-hr', color = 'blue', linestyle = 'dashed', linewidth=2)




#plt.plot([1.225, 1.225], [1, 0.9], color = 'black', label='1.225 tcc')
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
