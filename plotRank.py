import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yt

pix = 7880*3

ions = ['HI', 'MgII', 'CIII', 'CIV', 'NV', 'OVI', 'NevIII']

run1 = {'name':'M1-v480-T1-chem',
        't90':'0000',
        't75':'0000'}

runs = []
runs.append(run1)

#chem includes initial conditions at v0; so chem and tri should be off by one

for run in runs:
    for i, time in enumerate(['t90', 't75']):
        for ion in ions:
            #open files for plotting, ranked column densities
            chem = pd.read_csv('../rankNum/'+ion+'/chem'+run['name']+'_v'+str(i+1)+'.txt', header = None)
            tri = pd.read_csv('../rankNum/'+ion+'/tri'+run['name']+'_v'+str(i+1)+'.txt', header = None)

            #make projection plot
            data = yt.load('../'+run['name']+'/chkfiles/CT_hdf5_chk_'+time)
            data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun', sampling_type = 'cell')
            #add this ion
            _ = addfield(data, ion['atom'], ion['ion'], 'dens', source)

            #select the region
            reg = data.all_data()

            p = data.proj(ion[source], 1)

            #plot projection of ion
            p = yt.ProjectionPlot(data, 1, )


            x = np.arange(pix, 0, -1)/7880

            fig, ax = plt.subplots()
            ax.plot(x, chem[0][-pix:], color = 'blue', label = 'chem')
            ax.plot(x, tri[0][-pix:], color = 'red', label = 'tri', linestyle = 'dashed')
            ax.legend(loc=1)
            ax.set_yscale('log')
            ax.set_title('Y Proj')

            fig.savefig('../rankNum/'+ion+'/'+ion+'_'+run['name']+'_'+time+'.png')
