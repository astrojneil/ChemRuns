import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import yt
from yt.units import dimensions
import trident as tri
from massFracs import *
from yt.funcs import mylog
mylog.setLevel(40) # This sets the log level to "ERROR"

#chkfiles at 0.2tcc intervals
M1 = ['0000', '0002', '0005', '0008', '0011', '0014', '0017', '0021', '0025', '0027', '0030', '0033', '0036', '0038', '0041']
M6 = ['0000', '0002', '0006', '0011', '0015', '0019', '0023', '0028', '0032']

ChemList = M1
atom = 'C'
ion = 'III'
fieldtype = 'dens'
fieldname = fieldtype+atom+ion
savedir = 'M1-v480-T1-chem'

#usage of massFracs to add data
#addfield(data, atom, ion, fieldtype, datatype)

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

#settings for setting lowest value of colorbar to white
viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([255/256, 255/256, 255/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)


for i in ChemList:
    data = yt.load('../'+savedir+'/chkfiles/CT_hdf5_chk_'+i)
    #add metallicity for Trident estimation fraction fields
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name='Metallicity', units='Zsun')

    #add the fields you want to plot
    _ = addfield(data, atom, ion, fieldtype, 'chem')
    _ = addfield(data, atom, ion, fieldtype, 'tri')

    #print the fraction data to file
    #select the center of the simulations
    ad = data.sphere([0.0, 7.7e20, 0.0], (50., 'pc'))   #wind!
    #alldata = data.all_data()
    #ad  = alldata.cut_region(['obj["blob"] >= 0.9'])     #cloud!
    print('{:.4e}'.format(float(ad.mean('cjto'))))


    #plot trident fractions
    p = yt.ProjectionPlot(data, 'z', fieldname+'_tri', origin = 'native')
    p.set_zlim(fieldname+'_tri', 9e-5, 1.)
    p.set_cmap(fieldname+'_tri', cmap=newcmp)
    p.annotate_timestamp(text_args = {'color':'black'})
    p.save('../'+savedir+'/figures/Tri'+i+fieldname+'_proj.png')

    #plot MAIHEM fractions
    p2 = yt.ProjectionPlot(data, 'z', fieldname+'_chem', origin = 'native')
    p2.set_zlim(fieldname+'_chem', 9e-5, 1.)
    p2.set_cmap(fieldname+'_chem', cmap=newcmp)
    p2.annotate_timestamp(text_args = {'color':'black'})
    p2.save('../'+savedir+'/figures/Chem_'+i+'_'+fieldname+'_proj.png')

    #plot extra slices
    p3 = yt.ProjectionPlot(data, 'z', 'density', origin = 'native')
    p3.set_zlim('density', 1e-28, 1e-23)
    p3.save('../'+savedir+'/figures/'+i+'densProj.png')
