import matplotlib.pyplot as plt
import numpy as np
import yt
import trident as tri

def _CIVdensity(field, data):
    dens = data[(('flash', u'c3p '))]*data['density']
    return dens


for i in ['0000', '0001', '0002', '0003','0004', '0005', '0006', '0007', '0008','0009', '0010']:
    data = yt.load('../Chem_test/KH_hdf5_chk_'+i)

    #data.add_field(('gas', 'densCIV'), function=_CIVdensity, display_name="C IV Mass Density", units='g/cm^3')
    plot = yt.ProjectionPlot(data, 'z',  (('flash', 'c5p ')), origin = 'native')
    #plot.set_zlim('velocity_y', 1, 1e8)
    plot.annotate_timestamp()
    plot.annotate_grids()
    #plot.annotate_arrow((-1.636e20,  9.625e18,  1.829e20), length=0.06, plot_args={'color':'blue'})

    plot.save('ovi'+i+'.png')
