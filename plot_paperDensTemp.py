import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import yt
from yt.units import dimensions
import trident as tri
from mpl_toolkits.axes_grid1 import AxesGrid
from massFracs import *
from yt.funcs import mylog
mylog.setLevel(40) # This sets the log level to "ERROR"

kpc = 3.086e21 #cm

#define the runs and ions
run1 = {'Name':'M1-v480-T1-chem',
    'times': ['0030']}
run3 = {'Name':'M6.2-v3000-T1-chem',
    'times':['0100' ]}
run2 = {'Name':'M3.6-v3000-T3-chem',
    'times':['0110']}


run4 = {'Name':'T1_v480_chi1000',
    'times':['0009']}
run5 = {'Name':'T3_v3000_chi3000',
    'times':['0021']}
run6 = {'Name':'T1_v3000_chi1000',
    'times':['0022']}


#settings for setting lowest value of colorbar to white
viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([255/256, 255/256, 255/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)

fig = plt.figure()
grid = AxesGrid(fig, (0.1, 0.075, 0.85, 0.85),
            nrows_ncols = (2, 2),
            axes_pad = 0.05,
            cbar_size="3%",
            cbar_pad="2%",
            share_all=False,
            label_mode="1",
            cbar_location="right",
            cbar_mode="each")

run_new = run3
run_old = run6
for i in range(len(run_new['times'])):
    data1 = yt.load('../'+run_new['Name']+'/chkfiles/CT_hdf5_chk_'+run_new['times'][i])

    #open old run
    data2 = yt.load('/Volumes/GiantDrive1/Blob_paper1/Files/'+run_old['Name']+'/KH_hdf5_chk_'+run_old['times'][i])

    # Create the plot.  Since SlicePlot accepts a list of fields, we need only
    # do this once.
    fields = ['density', 'temperature']
    p1 = yt.SlicePlot(data1, 'z', fields, origin='native', width = (0.8, 'kpc'), center = (0, 0.4*kpc, 0))
    p1.set_cmap('all', cmap=newcmp)
    p1.set_zlim(fields[0], 1e-25, 1e-22)
    p1.set_zlim(fields[1], 1e4, 1e8)

    p2 = yt.SlicePlot(data2, 'z', fields, origin='native', width = (0.8, 'kpc'), center = (0, 0.4*kpc, 0))
    p2.set_cmap('all', cmap=newcmp)
    p2.set_zlim(fields[0], 1e-25, 1e-22)
    p2.set_zlim(fields[1], 1e4, 1e8)


    # For each plotted field, force the SlicePlot to redraw itself onto the AxesGrid
    for j, field in enumerate(fields):
        plot = p2.plots[field]
        plot.figure = fig
        plot.axes = grid[j].axes
        plot.axes.title = "Test"
        plot.cax = grid.cbar_axes[j]

    for j, field in enumerate(fields):
        plot = p1.plots[field]
        plot.figure = fig
        plot.axes = grid[j+2].axes
        plot.axes.title = "Test"
        plot.cax = grid.cbar_axes[j+2]


    # Finally, redraw the plot on the AxesGrid axes.
    p1._setup_plots()
    p2._setup_plots()

    plt.savefig('oldvnewDensTemp_'+run_new['Name']+'.png', tight_layout=True)
