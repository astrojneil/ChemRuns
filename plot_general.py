#general script to plot slices of a given field for a list of checkpoints for a given simulation

import matplotlib.pyplot as plt
import yt

dir = 'M1-v480-T1-chem'
chk = ['0001', '0005']

field = 'density'

for i in chk:
    data = yt.load('../'+dir+'/CT_hdf5_chk_'+i)
    p =  yt.SlicePlot(data, 'z', field, origin='native')

    p.save('../'+dir+'/figures/'+field+i+'.png')
