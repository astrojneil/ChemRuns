import matplotlib
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from massFracs import *
import yt


matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)

#settings for setting lowest value of colorbar to white
viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([255/256, 255/256, 255/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)




pix = 7880*3

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

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

ions = []
ions.append(ion1)
ions.append(ion2)
ions.append(ion3)
ions.append(ion4)
ions.append(ion5)
ions.append(ion6)
ions.append(ion7)

run1 = {'name':'M1-v480-T1-chem',
        't90':'0030',
        't75':'0041'}

runs = []
runs.append(run1)

#chem includes initial conditions at v0; so chem and tri should be off by one

for run in runs:
    for i, time in enumerate(['t90', 't75']):
        #make projection plot
        data = yt.load('../'+run['name']+'/chkfiles/CT_hdf5_chk_'+run[time])
        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun', sampling_type = 'cell')
        for ion in ions:
            #open files for plotting, ranked column densities
            chem = pd.read_csv('../rankNum/'+ion['name']+'/chem'+run['name']+'_v'+str(i+1)+'.txt', header = None)
            tri = pd.read_csv('../rankNum/'+ion['name']+'/tri'+run['name']+'_v'+str(i+1)+'.txt', header = None)

            #add this ion
            _ = addfield(data, ion['atom'], ion['ion'], 'dens', 'chem')

            #select the region
            reg = data.all_data()

            #plot projection of ion
            p = yt.ProjectionPlot(data, 1, ion['chem'], origin='native',  width=(0.6, 'kpc'))
            p.set_zlim(ion['chem'], 1e12, 1e18)
            p.set_cmap(ion['chem'], cmap=newcmp)

            p_plot = p.plots[ion['chem']]
            p_plot.hide_colorbar()
            p_plot.hide_axes()


            x = np.arange(pix, 0, -1)/7880

            #fig, ax = plt.subplots()
            fig = p_plot.figure
            ax1 = p_plot.axes
            ax1.set_position([0.15, 0.15, 0.35, 0.35])
            ax1.set_zorder(2)
            #p_plot.figure.set_figure(fig)
            left, bottom, width, height = [0.1, 0.1, 0.85, 0.85]
            ax = fig.add_axes([left, bottom, width, height], zorder = 1)

            ax.plot(x, chem[0][-pix:], color = 'blue', label = 'Chem', linewidth= 2)
            ax.plot(x, tri[0][-pix:], color = 'red', label = 'Trident', linestyle = 'dashed', linewidth=2)
            ax.legend(loc=1, fontsize = 20)
            ax.set_yscale('log')
            ax.set_title('Y Proj')
            ax.tick_params(length=6, width=2)

            fig.savefig('../rankNum/'+ion['name']+'/'+ion['name']+'_'+run['name']+'_'+time+'.png')
