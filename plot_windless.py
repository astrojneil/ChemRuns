import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import yt
from yt.units import dimensions
import trident as tri

ChemList = ['0000', '0005', '0010', '0015', '0016']
field = 'fracOVI'
savedir = 'M1-v480-T1-chem'

writefile = open('../'+savedir+'/massFracs_cloud.txt', 'w')
writefile.write('Chk, HI, MgII, CI, CII, CIII, CIV, CV, CVI, SiIII, SiIV, NV, OVI, NeVIII\n')

writefile_tri = open('../'+savedir+'/massFracs_cloud_tri.txt', 'w')
writefile_tri.write('Chk, HI, MgII, CI, CII, CIII, CIV, CV, CVI, SiIII, SiIV, NV, OVI, NeVIII\n')

viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
white = np.array([255/256, 255/256, 255/256, 1])
newcolors[:1, :] = white
newcmp = ListedColormap(newcolors)


###  HI mass fractions normalized by element
def _HIfrac_trident(field, data):
    dens = data['H_p0_density']/(data['H_p0_density']+data['H_p1_density'])
    return dens
def _HIfrac_chem(field, data):
    dens = data['h   ']/(data['h   ']+data['hp  '])
    return dens
def _HIdensity(field, data):
    dens = (data[(('flash', u'hp  '))]*data['density'])/(2.*1.6726219e-24)
    return dens


###  MgII mass fractions normalized by element
def _MgIIfrac_trident(field, data):
    dens = data['Mg_p1_density']/(data['Mg_p0_density']+data['Mg_p1_density']+data['Mg_p2_density']+data['Mg_p3_density']+data['Mg_p4_density']+data['Mg_p5_density'])
    return dens
def _MgIIfrac_chem(field, data):
    dens = data['mgp ']/(data['mg  ']+data['mgp ']+data['mg2p']+data['mg3p']+data['mg4p']+data['mg5p'])
    return dens
def _MgIIdensity(field, data):
    dens = (data[(('flash', u'mgp '))]*data['density'])/(24.*1.6726219e-24)
    return dens


###  CI mass fractions normalized by element
def _CIfrac_trident(field, data):
    dens = data['C_p0_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CIfrac_chem(field, data):
    dens = data['c   ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens


###  CII mass fractions normalized by element
def _CIIfrac_trident(field, data):
    dens = data['C_p1_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CIIfrac_chem(field, data):
    dens = data['cp  ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens
def _CIIdensity(field, data):
    dens = (data[(('flash', u'cp  '))]*data['density'])/(12.*1.6726219e-24)
    return dens


###  CIII mass fractions normalized by element
def _CIIIfrac_trident(field, data):
    dens = data['C_p2_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CIIIfrac_chem(field, data):
    dens = data['c2p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens
def _CIIIdensity(field, data):
    dens = (data[(('flash', u'c2p '))]*data['density'])/(12.*1.6726219e-24)
    return dens


###  CVI mass fractions normalized by element
def _CIVfrac_trident(field, data):
    dens = data['C_p3_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CIVfrac_chem(field, data):
    dens = data['c3p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens
def _CIVdensity(field, data):
    dens = (data[(('flash', u'c3p '))]*data['density'])/(12.*1.6726219e-24)
    return dens

###  CV mass fractions normalized by element
def _CVfrac_trident(field, data):
    dens = data['C_p4_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CVfrac_chem(field, data):
    dens = data['c4p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens
def _CVdensity(field, data):
    dens = (data[(('flash', u'c4p '))]*data['density'])/(12.*1.6726219e-24)
    return dens

###  CVI mass fractions normalized by element
def _CVIfrac_trident(field, data):
    dens = data['C_p5_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density']+data['C_p6_density'])
    return dens
def _CVIfrac_chem(field, data):
    dens = data['c5p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p ']+data['c6p '])
    return dens
def _CVIdensity(field, data):
    dens = (data[(('flash', u'c5p '))]*data['density'])/(12.*1.6726219e-24)
    return dens


###  SiIII mass fractions normalized by element
def _SiIIIfrac_trident(field, data):
    dens = data['Si_p2_density']/(data['Si_p0_density']+data['Si_p1_density']+data['Si_p2_density']+data['Si_p3_density']+data['Si_p4_density']+data['Si_p5_density'])
    return dens
def _SiIIIfrac_chem(field, data):
    dens = data['si2p']/(data['si  ']+data['sip ']+data['si2p']+data['si3p']+data['si4p']+data['si5p'])
    return dens
def _SiIIIdensity(field, data):
    dens = (data[(('flash', u'si2p'))]*data['density'])/(28.*1.6726219e-24)
    return dens


###  SiIV mass fractions normalized by element
def _SiIVfrac_trident(field, data):
    dens = data['Si_p3_density']/(data['Si_p0_density']+data['Si_p1_density']+data['Si_p2_density']+data['Si_p3_density']+data['Si_p4_density']+data['Si_p5_density'])
    return dens
def _SiIVfrac_chem(field, data):
    dens = data['si3p']/(data['si  ']+data['sip ']+data['si2p']+data['si3p']+data['si4p']+data['si5p'])
    return dens
def _SiIVdensity(field, data):
    dens = (data[(('flash', u'si3p'))]*data['density'])/(28.*1.6726219e-24)
    return dens


###  NV mass fractions normalized by element
def _NVfrac_trident(field, data):
    dens = data['N_p4_density']/(data['N_p0_density']+data['N_p1_density']+data['N_p2_density']+data['N_p3_density']+data['N_p5_density']+data['N_p6_density']+data['N_p7_density'])
    return dens
def _NVfrac_chem(field, data):
    dens = data['n4p ']/(data['n   ']+data['np  ']+data['n2p ']+data['n3p ']+data['n4p ']+data['n5p ']+data['n6p ']+data['n7p '])
    return dens
def _NVdensity(field, data):
    dens = (data[(('flash', u'n4p '))]*data['density'])/(14.*1.6726219e-24)
    return dens


###  OVI mass fractions normalized by element
def _OVIfrac_trident(field, data):
    dens = data['O_p5_density']/(data['O_p0_density']+data['O_p1_density']+data['O_p2_density']+data['O_p3_density']+data['O_p4_density']+data['O_p5_density']+data['O_p6_density']+data['O_p7_density']+data['O_p8_density'])
    return dens
def _OVIfrac_chem(field, data):
    dens = data['o5p ']/(data['o   ']+data['op  ']+data['o2p ']+data['o3p ']+data['o4p ']+data['o5p ']+data['o6p ']+data['o7p ']+data['o8p '])
    return dens
def _OVIdensity(field, data):
    dens = (data[(('flash', u'o5p '))]*data['density'])/(16.*1.6726219e-24)
    return dens


###  NeVIII mass fractions normalized by element
def _NeVIIIfrac_trident(field, data):
    dens = data['Ne_p7_density']/(data['Ne_p0_density']+data['Ne_p1_density']+data['Ne_p2_density']+data['Ne_p3_density']+data['Ne_p4_density']+data['Ne_p5_density']+data['Ne_p6_density']+data['Ne_p7_density']+data['Ne_p8_density']+data['Ne_p9_density'])
    return dens
def _NeVIIIfrac_chem(field, data):
    dens = data['ne7p']/(data['ne  ']+data['nep ']+data['ne2p']+data['ne3p']+data['ne4p']+data['ne5p']+data['ne6p']+data['ne7p']+data['ne8p']+data['ne9p'])
    return dens
def _NeVIIIdensity(field, data):
    dens = (data[(('flash', u'ne7p'))]*data['density'])/(20.*1.6726219e-24)
    return dens



#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")


for i in ChemList:
    data = yt.load('../'+savedir+'/CT_hdf5_chk_'+i)
    #pressure estimates:
    reg = data.all_data()
    maxPres = reg.max('pressure')
    minPres = reg.min('pressure')

    print('Max: '+str(maxPres))
    print('Min: '+str(minPres))
    print('ratio: '+str(minPres/maxPres))

    #add MAIHEM chemistry fraction fields
    data.add_field(('gas', 'fracHI'), function=_HIfrac_chem, display_name="H I Mass fraction", units="")
    data.add_field(('gas', 'fracMgII'), function=_MgIIfrac_chem, display_name="Mg II Mass fraction", units="")
    data.add_field(('gas', 'fracCI'), function=_CIfrac_chem, display_name="C I Mass fraction", units="")
    data.add_field(('gas', 'fracCII'), function=_CIIfrac_chem, display_name="C II Mass fraction", units="")
    data.add_field(('gas', 'fracCIII'), function=_CIIIfrac_chem, display_name="C III Mass fraction", units="")
    data.add_field(('gas', 'fracCIV'), function=_CIVfrac_chem, display_name="C IV Mass fraction", units="")
    data.add_field(('gas', 'fracCV'), function=_CVfrac_chem, display_name="C V Mass fraction", units="")
    data.add_field(('gas', 'fracCVI'), function=_CVIfrac_chem, display_name="C VI Mass fraction", units="")
    data.add_field(('gas', 'fracSiIII'), function=_SiIIIfrac_chem, display_name="Si III Mass fraction", units="")
    data.add_field(('gas', 'fracSiIV'), function=_SiIVfrac_chem, display_name="Si IV Mass fraction", units="")
    data.add_field(('gas', 'fracNV'), function=_NVfrac_chem, display_name="N V Mass fraction", units="")
    data.add_field(('gas', 'fracOVI'), function=_OVIfrac_chem, display_name="O VI Mass fraction", units="")
    data.add_field(('gas', 'fracNeVIII'), function=_NeVIIIfrac_chem, display_name="Ne VIII Mass fraction", units="")

    #add Trident estimation fraction fields
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name='Metallicity', units='Zsun')
    tri.add_ion_fields(data, ions=['H', 'Mg', 'C', 'N', 'O', 'Si', 'Ne'], ftype='gas')

    data.add_field(('gas', 'fracHI_tri'), function=_HIfrac_trident, display_name="H I Mass fraction", units="")
    data.add_field(('gas', 'fracMgII_tri'), function=_MgIIfrac_trident, display_name="Mg II Mass fraction", units="")
    data.add_field(('gas', 'fracCI_tri'), function=_CIfrac_trident, display_name="C I Mass fraction", units="")
    data.add_field(('gas', 'fracCII_tri'), function=_CIIfrac_trident, display_name="C II Mass fraction", units="")
    data.add_field(('gas', 'fracCIII_tri'), function=_CIIIfrac_trident, display_name="C III Mass fraction", units="")
    data.add_field(('gas', 'fracCIV_tri'), function=_CIVfrac_trident, display_name="C IV Mass fraction", units="")
    data.add_field(('gas', 'fracCV_tri'), function=_CVfrac_trident, display_name="C V Mass fraction", units="")
    data.add_field(('gas', 'fracCVI_tri'), function=_CVIfrac_trident, display_name="C VI Mass fraction", units="")
    data.add_field(('gas', 'fracSiIII_tri'), function=_SiIIIfrac_trident, display_name="Si III Mass fraction", units="")
    data.add_field(('gas', 'fracSiIV_tri'), function=_SiIVfrac_trident, display_name="Si IV Mass fraction", units="")
    data.add_field(('gas', 'fracNV_tri'), function=_NVfrac_trident, display_name="N V Mass fraction", units="")
    data.add_field(('gas', 'fracOVI_tri'), function=_OVIfrac_trident, display_name="O VI Mass fraction", units="")
    data.add_field(('gas', 'fracNeVIII_tri'), function=_NeVIIIfrac_trident, display_name="Ne VIII Mass fraction", units="")

    #print the fraction data to file
    #select the center of the simulations
    ad = data.sphere([0.0, 7.7e20, 0.0], (50., 'pc'))   #wind!

    #alldata = data.all_data()
    #ad  = alldata.cut_region(['obj["blob"] >= 0.9'])     #cloud!
    print('{:.4e}'.format(float(ad.mean('cjto'))))
    writefile.write(str(i)+', '+'{:.4e}'.format(float(ad.mean('fracHI')))+', '+'{:.4e}'.format(float(ad.mean('fracMgII')))+', '+'{:.4e}'.format(float(ad.mean('fracCI')))+', '+'{:.4e}'.format(float(ad.mean('fracCII')))+', '+'{:.4e}'.format(float(ad.mean('fracCIII')))+', '+'{:.4e}'.format(float(ad.mean('fracCIV')))+', '+'{:.4e}'.format(float(ad.mean('fracCV')))+', '+'{:.4e}'.format(float(ad.mean('fracCVI')))+', '+'{:.4e}'.format(float(ad.mean('fracSiIII')))+', '+'{:.4e}'.format(float(ad.mean('fracSiIV')))+', '+'{:.4e}'.format(float(ad.mean('fracNV')))+', '+'{:.4e}'.format(float(ad.mean('fracOVI')))+', '+'{:.4e}'.format(float(ad.mean('fracNeVIII')))+'\n')

    writefile_tri.write(str(i)+', '+'{:.4e}'.format(float(ad.mean('fracHI_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracMgII_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCI_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCII_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCIII_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCIV_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCV_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracCVI_tri')))+',  '+'{:.4e}'.format(float(ad.mean('fracSiIII_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracSiIV_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracNV_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracOVI_tri')))+', '+'{:.4e}'.format(float(ad.mean('fracNeVIII_tri')))+'\n')

    #plot trident fractions
    p = yt.SlicePlot(data, 'z', field+'_tri', origin = 'native')
    p.set_zlim(field+'_tri', 9e-5, 1.)
    p.set_cmap(field+'_tri', cmap=newcmp)
    p.annotate_timestamp()
    p.save('../'+savedir+'/Tri'+i+field+'.png')

    #plot MAIHEM fractions
    p2 = yt.SlicePlot(data, 'z', field, origin = 'native')
    p2.set_zlim(field, 9e-5, 1.)
    p2.set_cmap(field, cmap=newcmp)
    p2.annotate_timestamp()
    p2.save('../'+savedir+'/Chem_'+i+'_'+field+'.png')

    #plot extra slices
    p3 = yt.SlicePlot(data, 'z', 'density', origin = 'native')
    p3.set_zlim('density', 1e-28, 1e-23)
    p3.save('../'+savedir+'/'+i+'densSlice.png')

writefile.close()
writefile_tri.close()
