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

clouds = 5
size8 = 31436*clouds
size4 = 7859*clouds
size2 = 1965*clouds
size1 = 491*clouds


pc2 = 9.52e36 #cm^2
area8 = 1*pc2
area4 = 4*pc2
area2 = 16*pc2
area1 = 64*pc2

colors = {'H I 1215': black, 'Mg II':blu, 'C III':gre, 'C IV':blu, 'N V':gre, 'O VI':red, 'Ne VIII':pink}
style = {800:'solid', 400:'dashed', 200:'dotted', 100:'dashdot'}
machs = ['nocond', 'lowcond', 'cond'] #'m6_other']
#M1 = pd.read_csv('testRes_m1.csv')
#M6 = pd.read_csv('testRes_m6.csv')
#M3 = pd.read_csv('testRes_m3.csv')

 #M1


for i in range(len(machs)):
    fig, ax = plt.subplots(3,1,figsize = (9, 10))
    for j, ion in enumerate(['H I 1215','C IV','O VI']):
        M = pd.read_csv('testAngle_m6_'+machs[i]+'.csv')
        coldens_90 = M[ion+'_0.9']
        coldens_80 = M[ion+'_0.8']
        coldens_70 = M[ion+'_0.7']
        coldens_60 = M[ion+'_0.6']
        coldens_50 = M[ion+'_0.5']
        coldens_40 = M[ion+'_0.4']
        coldens_30 = M[ion+'_0.3']
        coldens_20 = M[ion+'_0.2']
        coldens_10 = M[ion+'_0.1']
        coldens_0 = M[ion+'_0']
        coldens_sort_90 = np.sort(np.log10(coldens_90))
        coldens_sort_80 = np.sort(np.log10(coldens_80))
        coldens_sort_70 = np.sort(np.log10(coldens_70))
        coldens_sort_60 = np.sort(np.log10(coldens_60))
        coldens_sort_50 = np.sort(np.log10(coldens_50))
        coldens_sort_40 = np.sort(np.log10(coldens_40))
        coldens_sort_30 = np.sort(np.log10(coldens_30))
        coldens_sort_20 = np.sort(np.log10(coldens_20))
        coldens_sort_10 = np.sort(np.log10(coldens_10))
        coldens_sort_0 = np.sort(np.log10(coldens_0))

        y4 = np.arange(len(coldens_sort_40[-size4:])+1, 1, -1)/(len(coldens_sort_40[-size4:])/clouds)


        ax[j].plot(coldens_sort_90[-size4:], y4, label='cos(theta) = 0.9 (~ x proj)', alpha = 1, color = colors[ion])
        ax[j].plot(coldens_sort_80[-size4:], y4, label='cos(theta) = 0.8', alpha = 1, color = colors[ion], linestyle = 'dashed')
        ax[j].plot(coldens_sort_70[-size4:], y4, label='cos(theta) = 0.7', alpha = 0.8, color = colors[ion])
        ax[j].plot(coldens_sort_60[-size4:], y4, label='cos(theta) = 0.6', alpha = 0.7, color = colors[ion], linestyle = 'dashed')
        ax[j].plot(coldens_sort_50[-size4:], y4, label='cos(theta) = 0.5', alpha = 0.5, color = colors[ion])
        ax[j].plot(coldens_sort_40[-size4:], y4, label='cos(theta) = 0.4', alpha = 0.5, color = colors[ion], linestyle = 'dashed')
        ax[j].plot(coldens_sort_30[-size4:], y4, label='cos(theta) = 0.3', alpha = 0.3, color = colors[ion])
        ax[j].plot(coldens_sort_20[-size4:], y4, label='cos(theta) = 0.2', alpha = 0.3, color = colors[ion], linestyle = 'dashed')
        ax[j].plot(coldens_sort_10[-size4:], y4, label='cos(theta) = 0.1', alpha = 0.1, color = colors[ion])
        ax[j].plot(coldens_sort_0[-size4:], y4, label='cos(theta) = 0 (y proj)', alpha = 0.1, color = colors[ion], linestyle = 'dashed')
        #ax[j].set_title('Mach {}'.format(machs[i][1:2]))
        ax[j].set_title(ion)
        ax[j].set_ylabel("Cloud Area", fontsize = 13)
        ax[j].set_xlim(8, 17)

    ax[0].set_ylim(0, clouds)
    ax[1].set_ylim(0, 5)
    ax[2].set_ylim(0, 3)
    ax[0].legend(bbox_to_anchor=(1.05, 1))
    #ax[0].set_ylim(0, 1)
    ax[2].set_xlabel('$\log(N_{ion})$', fontsize=13)
    plt.tight_layout()
    fig.savefig('testAngle'+machs[i]+'.png')
