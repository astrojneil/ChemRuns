#plot the velocity of the cloud as a function of time
#uses the global quantities outputted in *.dat

from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np


hydro = '../hydro/KH.dat'

plotName = 'Compare_velocity_withT_cool'

time_hydro = FLASHdat_retrieve(hydro, 'time/tcc')
vel_hydro = FLASHdat_retrieve(hydro, 'x-velocity_blob(>rho0/3.)')
frame_hydro = FLASHdat_retrieve(hydro, 'velframe')


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

#when you need to adjust due to frame changing:
#plt.plot(time_hydro_nc[ind[0]], (vel_hydro_nc[ind[0]]-(frame_hydro_nc[ind[0]]-1.7e8))/1e5, label='H-ad-hr', color = 'black', linestyle='dashed')


plt.xlim(0, 8.)
plt.ylim(0, 350)
plt.legend(loc=2, fontsize = 12)
plt.ylabel('Velocity (km/s)')
plt.xlabel('Time (tcc)')

fig = plt.gcf()
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig(plotName+'.pdf')
