import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

red = '#ea4646'
org = '#ecb03f'
gre = '#45ec3f'
blu = '#3fa2ec'
pur = '#b63fec'
black = 'black'
pink = 'magenta'

size = 7880*2

colors = {'H I': black, 'Mg II':blu, 'C III':org, 'C IV':red, 'N V':gre, 'O VI':pur, 'Ne VIII':pink}
style = {800:'solid', 400:'dashed', 200:'dotted', 100:'dashdot'}
res = [800, 400, 200, 100]
M1 = pd.read_csv('testRes_m1.csv')
M6 = pd.read_csv('testRes_m6.csv')
M3 = pd.read_csv('testRes_m3.csv')

 #M1
fig, ax = plt.subplots(4,1,figsize = (8, 8))

for ion in ['Mg II','C IV','O VI']:
    for i in range(len(res)):
        coldens_M1 = M1[ion+'_'+str(res[i])]
        coldens_M3 = M3[ion+'_'+str(res[i])]
        coldens_M6 = M6[ion+'_'+str(res[i])]
        coldens_sort_M1 = np.sort(np.log10(coldens_M1))
        coldens_sort_M3 = np.sort(np.log10(coldens_M3))
        coldens_sort_M6 = np.sort(np.log10(coldens_M6))

        #y2 = np.arange(len(coldens_sort_M1[-size:])+1, 1, -1)/(0.5*len(coldens_sort_M1[-size:]))
        y2 = np.arange(len(coldens_sort_M1)+1, 1, -1)/(0.5*len(coldens_sort_M1))

        #ax[i].plot(coldens_sort_M1[-size:], y2, label=ion+'_chem', color = colors[ion])
        #ax[i].plot(coldens_sort_M3[-size:], y2, label=ion+'_tri', linestyle = 'dashed', color = colors[ion])
        #ax[i].plot(coldens_sort_M6[-size:], y2, label=ion+'_tri', linestyle = 'dashed', color = colors[ion])

        ax[i].plot(coldens_sort_M1, y2, label=ion+'_M1', color = colors[ion])
        ax[i].plot(coldens_sort_M3, y2, label=ion+'_M3', color = colors[ion])
        ax[i].plot(coldens_sort_M6, y2, label=ion+'_M6', color = colors[ion])
        ax[i].set_title('Res {} x {}'.format(res[i], res[i]))
        ax[i].set_ylabel("Area Fraction", fontsize = 13)
        ax[i].set_xlim(12, 18)

ax[0].legend(bbox_to_anchor=(1.05, 1))
ax[1].set_xlim(12, 18)
#ax[0].set_ylim(0, 1)
ax[3].set_xlabel('$\log(N_{ion})$', fontsize=13)
plt.tight_layout()
fig.savefig('testRes.png')
