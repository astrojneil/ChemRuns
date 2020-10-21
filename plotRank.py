import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pix = 7880
ion = 'HI'
#chem includes initial conditions at v0; so chem and tri should be off by one
run_chem = 'M1-v480-T1-chem_v2'
run_tri = 'T1_v480_chi1000_v1'


#open files for plotting, ranked column densities
chem = pd.read_csv('../rankNum/'+ion+'/rankNum'+run_chem+'.txt', header = None)
tri = pd.read_csv('/Volumes/GiantDrive1/Blob_paper3/rankNum/'+ion+'/rankNum'+run_tri+'.txt', header = None)

x = np.arange(0, pix, 1)/pix

fig, ax = plt.subplots()
ax.plot(x, chem[0][-pix:], color = 'blue', label = 'chem')
ax.plot(x, tri[0][-pix:], color = 'red', label = 'tri', linestyle = 'dashed')
ax.legend(loc=2)

fig.savefig('../rankNum/'+ion+'/'+ion+'_M1_t75.png')
