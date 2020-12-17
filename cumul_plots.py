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

colors = {'HI': black, 'MgII':blu, 'CIII':org, 'CIV':red, 'NV':gre, 'OVI':pur, 'NeVIII':pink}
chem_M1 = pd.read_csv('../M1-v480-T1-chem/M1-v480-T1-chem_coldens_chem.csv')
chem_M6 = pd.read_csv('../M6.3-v3000-T1-chem/M6.2-v3000-T1-chem_coldens_chem.csv')

tri_M1 = pd.read_csv('../M1-v480-T1-chem/M1-v480-T1-chem_coldens_tri.csv')
tri_M6 = pd.read_csv('../M6.3-v3000-T1-chem/M6.2-v3000-T1-chem_coldens_tri.csv')

 #M1
fig, ax = plt.subplots(2,1,figsize = (8, 8))

for ion in ['HI', 'MgII', 'CIII', 'CIV', 'NV', 'OVI', 'NeVIII']:
    for i in [0, 1]:
        coldens_chem = chem_M1[ion+'_'+str(i)]
        coldens_tri = tri_M1[ion+'_'+str(i)]
        coldens_sort_chem = np.sort(np.log10(coldens_chem))
        coldens_sort_tri = np.sort(np.log10(coldens_tri))

        y2 = np.arange(len(coldens_sort_chem[-size:])+1, 1, -1)/(0.5*len(coldens_sort_chem[-size:]))

        ax[i].plot(coldens_sort_chem[-size:], y2, label=ion+'_chem', color = colors[ion])
        ax[i].plot(coldens_sort_tri[-size:], y2, label=ion+'_tri', linestyle = 'dashed', color = colors[ion])

ax[0].set_xlim(12, 18)
#ax[1].set_ylim(0, 1)
ax[0].legend(bbox_to_anchor=(1.05, 1))
ax[1].set_xlim(12, 18)
#ax[0].set_ylim(0, 1)
ax[0].set_title("M1-v480-T1-chem - init", fontsize = 13)
ax[0].set_ylabel("Cloud Fraction", fontsize = 13)
ax[1].set_ylabel("Cloud Fraction", fontsize = 13)
ax[1].set_title("3 tcc", fontsize =13)
ax[1].set_xlabel('$\log(N_{ion})$', fontsize=13)
plt.tight_layout()
fig.savefig('M1_chemVtri.png')


 #M6
fig, ax = plt.subplots(2,1, figsize = (8, 8))

for ion in ['HI', 'MgII', 'CIII', 'CIV', 'NV', 'OVI', 'NeVIII']:
    for i in [0, 1]:
        coldens_chem = chem_M6[ion+'_'+str(i)]
        coldens_tri = tri_M6[ion+'_'+str(i)]
        coldens_sort_chem = np.sort(np.log10(coldens_chem))
        coldens_sort_tri = np.sort(np.log10(coldens_tri))

        y2 = np.arange(len(coldens_sort_chem[-size:])+1, 1, -1)/(0.5*len(coldens_sort_chem[-size:]))

        ax[i].plot(coldens_sort_chem[-size:], y2, label=ion+'_chem', color = colors[ion])
        ax[i].plot(coldens_sort_tri[-size:], y2, label=ion+'_tri', linestyle = 'dashed', color = colors[ion])

ax[0].set_xlim(10, 20)
#ax[1].set_ylim(0, 1)
#ax[0].legend(bbox_to_anchor=(1.05, 1))
ax[1].set_xlim(10, 20)
#ax[0].set_ylim(0, 1)
ax[0].set_title("M6-v3000-T1-chem - init", fontsize = 13)
ax[0].set_ylabel("Cloud Fraction", fontsize = 13)
ax[1].set_ylabel("Cloud Fraction", fontsize = 13)
ax[1].set_title("3 tcc", fontsize =13)
ax[1].set_xlabel('$\log(N_{ion})$', fontsize=13)
plt.tight_layout()
fig.savefig('M6_chemVtri.png')
