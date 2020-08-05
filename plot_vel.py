#plot the velocity of the cloud as a function of time
#uses the global quantities outputted in *.dat

from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np


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

b10_t_nc = '/Volumes/GiantDrive2/MHD_overflow/B10_T_noCool_highres/KH.dat'
b10_a_nc = '/Volumes/GiantDrive2/MHD_overflow/B10_A_noCool_highres/KH.dat'
hydro_nc = '/Volumes/GiantDrive2/MHD_overflow/Hydro_noCool/KH.dat'

plotName = 'Compare_velocity_withT_cool'

time_hydro = FLASHdat_retrieve(hydro, 'time/tcc')
vel_hydro = FLASHdat_retrieve(hydro, 'x-velocity_blob(>rho0/3.)')
frame_hydro = FLASHdat_retrieve(hydro, 'velframe')

time_hydro_lr = FLASHdat_retrieve(hydro_lr, 'time/tcc')
vel_hydro_lr = FLASHdat_retrieve(hydro_lr, 'x-velocity_blob(>rho0/3.)')
frame_hydro_lr = FLASHdat_retrieve(hydro_lr, 'velframe')

time_hydro_nc = FLASHdat_retrieve(hydro_nc, 'time/tcc')
vel_hydro_nc = FLASHdat_retrieve(hydro_nc, 'x-velocity_blob(>rho0/3.)')
frame_hydro_nc = FLASHdat_retrieve(hydro_nc, 'velframe')


time_b10_a = FLASHdat_retrieve(b10_a, 'time/tcc')
vel_b10_a = FLASHdat_retrieve(b10_a, 'x-velocity_blob(>rho0/10.)')
frame_b10_a = FLASHdat_retrieve(b10_a, 'velframe')

time_b10_a_nc = FLASHdat_retrieve(b10_a_nc, 'time/tcc')
vel_b10_a_nc = FLASHdat_retrieve(b10_a_nc, 'x-velocity_blob(>rho0/10.)')
frame_b10_a_nc = FLASHdat_retrieve(b10_a_nc, 'velframe')

time_b10_t = FLASHdat_retrieve(b10_t, 'time/tcc')
vel_b10_t = FLASHdat_retrieve(b10_t, 'x-velocity_blob(>rho0/10.)')
frame_b10_t = FLASHdat_retrieve(b10_t, 'velframe')

time_b10_t_nc = FLASHdat_retrieve(b10_t_nc, 'time/tcc')
vel_b10_t_nc = FLASHdat_retrieve(b10_t_nc, 'x-velocity_blob(>rho0/10.)')
frame_b10_t_nc = FLASHdat_retrieve(b10_t_nc, 'velframe')

time_b10_t_lr = FLASHdat_retrieve(b10_t_lr, 'time/tcc')
vel_b10_t_lr = FLASHdat_retrieve(b10_t_lr, 'x-velocity_blob(>rho0/10.)')
frame_b10_t_lr = FLASHdat_retrieve(b10_t_lr, 'velframe')

time_b10_a_lr = FLASHdat_retrieve(b10_a_lr, 'time/tcc')
vel_b10_a_lr = FLASHdat_retrieve(b10_a_lr, 'x-velocity_blob(>rho0/10.)')
frame_b10_a_lr = FLASHdat_retrieve(b10_a_lr, 'velframe')



#calc blob vel:
def calc_vel(vel_list, frame_list, time_list):
    vels = []
    oldFrame = 0
    extraFrame = 0
    oldTime = 0
    for i in range(len(vel_list)):
        newFrame = frame_list[i]

        if newFrame != oldFrame:
            if newFrame < 0: #take out long solid bar
                extraFrame = extraFrame
            else:
                if time_list[i] >5.8002055:
                    print('blah!')
                    extraFrame = extraFrame
                else:
                    extraFrame = extraFrame + oldFrame

            oldFrame = newFrame
            oldTime =  time_list[i]

        vel = vel_list[i] + newFrame + extraFrame
        vels.append(vel)

    vels = np.array(vels)
    print(len(vels))
    return vels

vels = calc_vel(vel_b10_t, frame_b10_t, time_b10_t)
vels_nc = calc_vel(vel_b10_t_nc, frame_b10_t_nc, time_b10_t_nc)
ind = np.where(time_hydro_nc< 4.0)

plt.plot(time_hydro, (vel_hydro+frame_hydro)/1e5, label = 'H-rad-hr', color = 'black')
#plt.plot(time_hydro_lr, (vel_hydro_lr+frame_hydro_lr)/1e5, label = 'H-rad-lr', color = 'black', linestyle = 'dotted', linewidth = 2)

plt.plot(time_hydro_nc[ind[0]], (vel_hydro_nc[ind[0]]-(frame_hydro_nc[ind[0]]-1.7e8))/1e5, label='H-ad-hr', color = 'black', linestyle='dashed')

plt.plot(time_b10_a, (vel_b10_a+frame_b10_a)/1e5, label='A-rad-hr', color = 'red')
#plt.plot(time_b10_a_lr, (vel_b10_a_lr+frame_b10_a_lr)/1e5, label = 'A-rad-lr', color = 'red', linestyle = 'dotted', linewidth=2)

plt.plot(time_b10_a_nc, (vel_b10_a_nc+frame_b10_a_nc)/1e5, label='A-ad-hr', color = 'red', linestyle='dashed')

#plt.plot(time_b10_t, (vel_b10_t+frame_b10_t)/1e5, label='T-hr', color = 'blue')

#plt.plot(time_b10_t_nc, (vel_b10_t_nc+frame_b10_t_nc)/1e5, label='T-hr-nc', color = 'blue', linestyle = 'dashed')

plt.plot(time_b10_t, vels/1e5, label='T-rad-hr', color = 'blue')
#plt.plot(time_b10_t_lr, (vel_b10_t_lr+frame_b10_t_lr)/1e5, label = 'T-rad-lr', color='blue', linestyle = 'dotted', linewidth = 2)

plt.plot(time_b10_t_nc, vels_nc/1e5, label='T-ad-hr', color = 'blue', linestyle = 'dashed')

plt.xlim(0, 8.)
plt.ylim(0, 350)
plt.legend(loc=2, fontsize = 12)
plt.ylabel('Velocity (km/s)')
plt.xlabel('Time (tcc)')

fig = plt.gcf()
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig(plotName+'.pdf')
