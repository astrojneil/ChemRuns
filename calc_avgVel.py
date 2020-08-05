#calculates the average velocity of the cloud through time
#by opening each checkpoint file

#this is a work around for not having average velocity in the global quantities

import numpy as np
import yt
import matplotlib.pyplot as plt

cloudMass =1.223869564736320599e38
#blobRho field
def _blobRho(field, data):
    dens = data['blob']*data['density']
    return dens

outfile = open('avgVel_B10A_hr.txt', 'a')


dir = 'M3.5_B10_A_highres'
runList = ['0000', '0001', '0003', '0006', '0010', '0014', '0017', '0022', '0026', '0029', '0033', '0037', '0040', '0044', '0046', '0050', '0052', '0055', '0058', '0060', '0063', '0066']

i = 1
#start loop through available chk files
for run in runList:
    #data = yt.load('/Volumes/GiantDrive2/Blob_paper1/Files/T1_v1700_chi1000_lref4/KH_hdf5_chk_'+run)
    data = yt.load('../'+dir+'/KH_hdf5_chk_'+run)

    #create blobRho field
    data.add_field(('gas', 'blobRho'), function=_blobRho, display_name="Cloud Density", units="g/cm**3")

    #select region with 0.1 < blob < 0.9
    alldata = data.all_data()
    ad_less9 = alldata.cut_region(['obj["blob"] <= 0.9'])
    ad_great1 = ad_less9.cut_region(['obj["blob"] >= 0.1'])

    #sum (~ volume integral) of the selected region
    blobRho = ad_great1['blobRho']
    dv = ad_great1['cell_volume']
    velx = abs(ad_great1['velx'])
    vely = abs(ad_great1['vely'])
    velz = abs(ad_great1['velz'])

    inner_intx = blobRho*dv*velx
    inner_inty = blobRho*dv*vely
    inner_intz = blobRho*dv*velz

    avgVelx = np.trapz(inner_intx)/cloudMass
    avgVely = np.trapz(inner_inty)/cloudMass
    avgVelz = np.trapz(inner_intz)/cloudMass

    #save value and time in tcc
    outfile.write(str(data.current_time.in_units('Myr').value)+' '+str(avgVelx.value)+' '+str(avgVely.value)+' '+str(avgVelz.value)+'\n')
    data.index.clear_all_data()
    alldata.index.clear_all_data()
    ad_less9.index.clear_all_data()
    ad_great1.index.clear_all_data()

    print('Finished with file '+str(i))
    i = i+1
#end of loop through files

outfile.close()
