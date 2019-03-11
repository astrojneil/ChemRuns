import matplotlib.pyplot as plt
import numpy as np
import yt
import trident as tri

def _CIVdensity(field, data):
    dens = data[(('flash', u'c3p '))]*data['density']
    return dens


for i in ['0000', '0005', '0010', '0015', '0020', '0025', '0030', '0035', '0040']:
#for i in ['0000', '0004', '0010', '0014', '0020', '0024']:
#for i in ['0000', '0005', '0010', '0015', '0020', '0025', '0030', '0035']:
#for i in ['0000', '0003', '0006', '0009', '0012', '0015', '0018', '0021', '0024', '0027', '0030', '0033', '0036']:
    data = yt.load('../inflowTests/inflowMach3/KH_hdf5_chk_'+i)
    #center = data.domain_center
    #for size in [50, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600]:
        #left_corner = data.domain_left_edge
        #right_corner = data.domain_right_edge

        #depth = data.quan(size, 'pc')
        #left_corner[2] = center[2]-0.5*depth
        #right_corner[2] = center[2] + 0.5*depth

        #region = data.box(left_corner, right_corner)
        #data.add_field(('gas', 'densCIV'), function=_CIVdensity, display_name="C IV Mass Density", units='g/cm^3')
        #plot = yt.ProjectionPlot(data, 'z',  (('flash', u'c3p ')), origin = 'native', data_source = region)
    plot = yt.ProjectionPlot(data, 'z',  (('flash', u'c3p ')), origin = 'native')
    #plot = yt.ProjectionPlot(data, 'z',  'temperature', origin = 'native')
    #plot.set_zlim((('flash', u'c3p ')), 5e13, 5e14)
    #plot.set_zlim('density', 1e-24, 1e-28)
    #plot = yt.SlicePlot(data, 'z', 'density', origin ='native')
    plot.annotate_timestamp()
    plot.annotate_grids()
        #plot.annotate_arrow((-1.636e20,  9.625e18,  1.829e20), length=0.06, plot_args={'color':'blue'})

        #plot.save('slice'+i+'_'+str(size)+'.png')
    plot.save('inflow_civ'+i+'.png')

    plot1 = yt.ProjectionPlot(data, 'x',  (('flash', u'c3p ')), origin = 'native')
    #plot1 = yt.ProjectionPlot(data, 'x',  'temperature', origin = 'native')
    #plot.set_zlim((('flash', u'c3p ')), 5e13, 5e14)
    #plot.set_zlim('density', 1e-24, 1e-28)
    #plot = yt.SlicePlot(data, 'z', 'density', origin ='native')
    plot1.annotate_timestamp()
    plot1.annotate_grids()
        #plot.annotate_arrow((-1.636e20,  9.625e18,  1.829e20), length=0.06, plot_args={'color':'blue'})

        #plot.save('slice'+i+'_'+str(size)+'.png')
    plot1.save('inflowx_civ'+i+'.png')

    plot2 = yt.ProjectionPlot(data, 'y',  (('flash', u'c3p ')), origin = 'native')
    #plot2 = yt.ProjectionPlot(data, 'y',  'temperature', origin = 'native')
    #plot.set_zlim((('flash', u'c3p ')), 5e13, 5e14)
    #plot.set_zlim('density', 1e-24, 1e-28)
    #plot = yt.SlicePlot(data, 'z', 'density', origin ='native')
    plot2.annotate_timestamp()
    plot2.annotate_grids()
        #plot.annotate_arrow((-1.636e20,  9.625e18,  1.829e20), length=0.06, plot_args={'color':'blue'})

        #plot.save('slice'+i+'_'+str(size)+'.png')
    plot2.save('inflowy_civ'+i+'.png')
