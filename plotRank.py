import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#open files for plotting, ranked column densities
chem = pd.read_csv('../rankNum/MgII/rankNumM6.2-v3000-T1-chem_v1.txt', header = None)
tri = pd.read_csv('/Volumes/GiantDrive1/Blob_paper3/rankNum/MgII/rankNumT1_v3000_chi1000_v1.txt', header = None)

x = np.arange(0, 7880, 1)/7880

fig, ax = plt.subplots()
ax.plot(x, chem[0][-7880:], color = 'blue', label = 'chem')
ax.plot(x, tri[0][-7880:], color = 'red', label = 'tri', linestyle = 'dashed')
ax.legend(loc=2)

fig.savefig('MgII_M6.png')
