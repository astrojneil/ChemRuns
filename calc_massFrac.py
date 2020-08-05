#calculates the mass fraction of the cloud through time
#by opening each checkpoint file

#this is a work around for not having mass fraction in the global quantities

import numpy as np
import yt
import matplotlib.pyplot as plt

cloudMass =1.223869564736320599e38
#blobRho field
def _blobRho(field, data):
    dens = data['blob']*data['density']
    return dens

outfile = open('massFrac_B10T_hr.txt', 'a')

runList = ['0000', '0001', '0003', '0006', '0010', '0014', '0017', '0022', '0026', '0029', '0033', '0037', '0040', '0044', '0046', '0050', '0052', '0055', '0058', '0060', '0063', '0066']
dir = 'M3.5_B10_T_highres'

 #['0000', '0004', '0009', '0016', '0022', '0025', '0027', '0028', '0029', '0030', '0032', '0033', '0034', '0035', '0036', '0037', '0038', '0039', '0041', '0042', '0043', '0044', '0046', '0047', '0048', '0049', '0051', '0052', '0053', '0054', '0056', '0057', '0058', '0060', '0061', '0063', '0064', '0065', '0067', '0068']

i = 1
#start loop through available chk files
for run in runList:
    #data = yt.load('/Volumes/GiantDrive2/Blob_paper1/Files/T1_v1700_chi1000_lref4/KH_hdf5_chk_'+run)
    data = yt.load('../'+dir+'/KH_hdf5_chk_'+run)

    #create blobRho field
    #data.add_field(('gas', 'blobRho'), function=_blobRho, display_name="Cloud Density", units="g/cm**3")

    #select regions with rho>rho_c/3
    alldata = data.all_data()
    ad_dense = alldata.cut_region(['obj["density"] >= 3.33e-25'])


    #sum (~ volume integral) of the selected region
    denseGas = ad_dense['density']
    dv = ad_dense['cell_volume']

    inner_int = denseGas*dv

    massFrac = np.trapz(inner_int)

    #normalize by blob initial mass
    normMassFrac = massFrac/cloudMass

    #save value and time in tcc
    outfile.write(str(data.current_time.in_units('Myr').value)+' '+str(normMassFrac.value)+'\n')
    data.index.clear_all_data()
    alldata.index.clear_all_data()
    ad_dense.index.clear_all_data()

    print('Finished with file '+str(i))
    i = i+1
#end of loop through files

outfile.close()
