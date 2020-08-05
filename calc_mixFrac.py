#calculates the mixing fraction of the cloud through time
#by opening each checkpoint file

#this is a work around for not having mixing fraction in the global quantities

import numpy as np
import yt
import matplotlib.pyplot as plt

cloudMass =1.223869564736320599e38
#blobRho field
def _blobRho(field, data):
    dens = data['blob']*data['density']
    return dens

outfile = open('txtFiles/mixFrac_B1_A_hr.txt', 'a')
dir = 'M3.5_B1_A'

runList = ['0000', '0001', '0002', '0003', '0005', '0006', '0007', '0008', '0009', '0011', '0012', '0013', '0015', '0016', '0018', '0019', '0021', '0022', '0024', '0025', '0027', '0029', '0031', '0033', '0035', '0038', '0039', '0040', '0043', '0046', '0051', '0058']

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

    inner_int = blobRho*dv

    mixFrac = np.trapz(inner_int)

    #normalize by blob initial mass
    normMixFrac = mixFrac/cloudMass

    #save value and time in tcc
    outfile.write(str(data.current_time.in_units('Myr').value)+' '+str(normMixFrac.value)+'\n')
    data.index.clear_all_data()
    alldata.index.clear_all_data()
    ad_less9.index.clear_all_data()
    ad_great1.index.clear_all_data()

    print('Finished with file '+str(i))
    i = i+1
#end of loop through files

outfile.close()
