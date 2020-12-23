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

clouds = 4
size8 = round(31436*clouds)
size4 = round(7859*clouds)
size2 = round(1965*clouds)
size1 = round(491*clouds)


pc2 = 9.52e36 #cm^2
area8 = 1*pc2
area4 = 4*pc2
area2 = 16*pc2
area1 = 64*pc2

colors = {'H I 1215': black, 'Mg II':blu, 'C III':gre, 'C IV':blu, 'N V':red, 'O VI':gre, 'Ne VIII':pink}
style = {800:'solid', 400:'dashed', 200:'dotted', 100:'dashdot'}
machs = ['m1', 'm3', 'm6_other']
#M1 = pd.read_csv('testRes_m1.csv')
#M6 = pd.read_csv('testRes_m6.csv')
#M3 = pd.read_csv('testRes_m3.csv')

 #M1
fig, ax = plt.subplots(3,1,figsize = (9, 10))

for ion in ['H I 1215','C IV','O VI']:
    for i in range(len(machs)):
        M = pd.read_csv('testRes_'+machs[i]+'.csv')
        coldens_800 = M[ion+'_800']
        coldens_400 = M[ion+'_400']
        coldens_200 = M[ion+'_200']
        coldens_100 = M[ion+'_100']
        coldens_sort_800 = np.sort(np.log10(coldens_800))
        coldens_sort_400 = np.sort(np.log10(coldens_400))
        coldens_sort_200 = np.sort(np.log10(coldens_200))
        coldens_sort_100 = np.sort(np.log10(coldens_100))

        #y = np.arange(len(coldens_sort_M1[-size:])+1, 1, -1)/(0.5*len(coldens_sort_M1[-size:]))
        y8 = np.arange(len(coldens_sort_800[-size8:])+1, 1, -1)/(len(coldens_sort_800[-size8:])/clouds)
        y4 = np.arange(len(coldens_sort_400[-size4:])+1, 1, -1)/(len(coldens_sort_400[-size4:])/clouds)
        y2 = np.arange(len(coldens_sort_200[-size2:])+1, 1, -1)/(len(coldens_sort_200[-size2:])/clouds)
        y1 = np.arange(len(coldens_sort_100[-size1:])+1, 1, -1)/(len(coldens_sort_100[-size1:])/clouds)

        #test mass conservation
        col_sort_800 = np.sort(coldens_800)
        col_sort_400 = np.sort(coldens_400)
        col_sort_200 = np.sort(coldens_200)
        col_sort_100 = np.sort(coldens_100)
        print(ion)
        print('M{}'.format(machs[i][1:2]))
        print('800: {}'.format(np.average(coldens_sort_800[-(size8):])))
        print('400: {}'.format(np.average(coldens_sort_400[-(size4):])))
        print('200: {}'.format(np.average(coldens_sort_200[-(size2):])))
        print('100: {}'.format(np.average(coldens_sort_100[-(size1):])))
        #print('800: {}'.format(np.sum(col_sort_800[-size8:]*area8)))
        #print('400: {}'.format(np.sum(col_sort_400[-size4:]*area4)))
        #print('200: {}'.format(np.sum(col_sort_200[-size2:]*area2)))
        #print('100: {}'.format(np.sum(col_sort_100[-size1:]*area1)))

        #plot
        large100 = []
        for m in np.arange(0, size1):
            for j in range(64):
                large100.append(coldens_sort_100[-size1:][m])
        #coldens_sort_800[-size8:][64*np.arange(0, 1*491)]
        restest = coldens_sort_800[-size8:][-125696:] - large100[-125696:]
        ax[i].plot(coldens_sort_800[-size8:][-125696:], np.log10(large100[-125696:]*(10**restest)), label=ion+'(800-100)', color = colors[ion])
        #ax[i].hist(coldens_sort_800[-size8:], bins =70, label = ion+'_800')
        #ax[i].hist(coldens_sort_400[-size4:], bins = 70, label = ion+'_400')

        #ax[i].plot(coldens_sort_800[-size8:], y8, label=ion+'_800', color = colors[ion])
        #ax[i].plot(coldens_sort_400[-size4:], y4, label=ion+'_400', linestyle = 'dashed', color = colors[ion])
        #ax[i].plot(coldens_sort_200[-size2:], y2, label=ion+'_200', linestyle = 'dotted', color = colors[ion])
        #ax[i].plot(coldens_sort_100[-size1:], y1, label=ion+'_100', linestyle = 'dashdot', color = colors[ion])
        ax[i].set_title('Mach {}'.format(machs[i][1:2]))
        ax[i].set_ylabel("$\log(N_{800} - N_{100})$", fontsize = 13)
        ax[i].set_xlim(8, 17)
        #ax[i].set_yscale('log')
        ax[i].set_ylim(-0.1, 1.4)

#ax[0].set_ylim(0, clouds)
#ax[1].set_ylim(0, 4)
#ax[2].set_ylim(0, 1.5)
ax[0].legend(bbox_to_anchor=(1.05, 1))
#ax[0].set_ylim(0, 1)
ax[2].set_xlabel('$\log(N_{ion})$', fontsize=13)
plt.tight_layout()
fig.savefig('resdiff.png')
