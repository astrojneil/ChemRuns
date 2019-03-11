import numpy as np
import matplotlib.pyplot as plt
import yt
from yt.units import dimensions
import trident as tri

ChemList = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007']#['0000', '0005', '0010', '0015']#, '0020']
nonChemList = []#['0000', '0010', '0050', '0100', '0130']
savedir = 'CI'
noChemField = 'fracCI'
ChemField = ''

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
    dens = data['Mg_p1_density']/(data['Mg_p0_density']+data['Mg_p1_density']+data['Mg_p2_density']+data['Mg_p3_density'])
    return dens
def _MgIIfrac_chem(field, data):
    dens = data['mgp ']/(data['mg  ']+data['mgp ']+data['mg2p']+data['mg3p'])
    return dens
def _MgIIdensity(field, data):
    dens = (data[(('flash', u'mgp '))]*data['density'])/(24.*1.6726219e-24)
    return dens


###  CI mass fractions normalized by element
def _CIfrac_trident(field, data):
    dens = data['C_p0_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density'])
    return dens
def _CIfrac_chem(field, data):
    dens = data['c   ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p '])
    return dens


###  CII mass fractions normalized by element
def _CIIfrac_trident(field, data):
    dens = data['C_p1_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density'])
    return dens
def _CIIfrac_chem(field, data):
    dens = data['cp  ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p '])
    return dens
def _CIIdensity(field, data):
    dens = (data[(('flash', u'cp  '))]*data['density'])/(12.*1.6726219e-24)
    return dens


###  CIII mass fractions normalized by element
def _CIIIfrac_trident(field, data):
    dens = data['C_p2_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density'])
    return dens
def _CIIIfrac_chem(field, data):
    dens = data['c2p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p '])
    return dens
def _CIIIdensity(field, data):
    dens = (data[(('flash', u'c2p '))]*data['density'])/(12.*1.6726219e-24)
    return dens


###  CVI mass fractions normalized by element
def _CIVfrac_trident(field, data):
    dens = data['C_p3_density']/(data['C_p0_density']+data['C_p1_density']+data['C_p2_density']+data['C_p3_density']+data['C_p4_density']+data['C_p5_density'])
    return dens
def _CIVfrac_chem(field, data):
    dens = data['c3p ']/(data['c   ']+data['cp  ']+data['c2p ']+data['c3p ']+data['c4p ']+data['c5p '])
    return dens
def _CIVdensity(field, data):
    dens = (data[(('flash', u'c3p '))]*data['density'])/(12.*1.6726219e-24)
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
    dens = data['N_p4_density']/(data['N_p0_density']+data['N_p1_density']+data['N_p2_density']+data['N_p3_density']+data['N_p5_density']+data['N_p6_density'])
    return dens
def _NVfrac_chem(field, data):
    dens = data['n4p ']/(data['n   ']+data['np  ']+data['n2p ']+data['n3p ']+data['n4p ']+data['n5p ']+data['n6p '])
    return dens
def _NVdensity(field, data):
    dens = (data[(('flash', u'n4p '))]*data['density'])/(14.*1.6726219e-24)
    return dens


###  OVI mass fractions normalized by element
def _OVIfrac_trident(field, data):
    dens = data['O_p5_density']/(data['O_p0_density']+data['O_p1_density']+data['O_p2_density']+data['O_p3_density']+data['O_p4_density']+data['O_p5_density']+data['O_p6_density']+data['O_p7_density'])
    return dens
def _OVIfrac_chem(field, data):
    dens = data['o5p ']/(data['o   ']+data['op  ']+data['o2p ']+data['o3p ']+data['o4p ']+data['o5p ']+data['o6p ']+data['o7p '])
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


for i in nonChemList:
    data = yt.load('../windless_nochem/KH_hdf5_chk_'+i)
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name='Metallicity', units='Zsun')

    tri.add_ion_fields(data, ions=['H', 'Mg', 'C', 'N', 'O', 'Si', 'Ne'], ftype='gas')

    data.add_field(('gas', 'fracHI'), function=_HIfrac_trident, display_name="H I Mass fraction", units="")
    data.add_field(('gas', 'fracMgII'), function=_MgIIfrac_trident, display_name="Mg II Mass fraction", units="")
    data.add_field(('gas', 'fracCI'), function=_CIfrac_trident, display_name="C I Mass fraction", units="")
    data.add_field(('gas', 'fracCII'), function=_CIIfrac_trident, display_name="C II Mass fraction", units="")
    data.add_field(('gas', 'fracCIII'), function=_CIIIfrac_trident, display_name="C III Mass fraction", units="")
    data.add_field(('gas', 'fracCIV'), function=_CIVfrac_trident, display_name="C IV Mass fraction", units="")
    data.add_field(('gas', 'fracSiIII'), function=_SiIIIfrac_trident, display_name="Si III Mass fraction", units="")
    data.add_field(('gas', 'fracSiIV'), function=_SiIVfrac_trident, display_name="Si IV Mass fraction", units="")
    data.add_field(('gas', 'fracNV'), function=_NVfrac_trident, display_name="N V Mass fraction", units="")
    data.add_field(('gas', 'fracOVI'), function=_OVIfrac_trident, display_name="O VI Mass fraction", units="")
    data.add_field(('gas', 'fracNeVIII'), function=_NeVIIIfrac_trident, display_name="Ne VIII Mass fraction", units="")

    #p = yt.SlicePlot(data, 'z', 'temperature', origin = 'native')
    p = yt.SlicePlot(data, 'z', noChemField, origin = 'native')
    p.set_zlim(noChemField, 1e-4, 1.)
    p.annotate_timestamp()
    #p.save('windlessPlots/noChem'+i+'_'+savedir+'.png')


for i in ChemList:
    data = yt.load('../Chem_test/KH_hdf5_chk_'+i)

    reg = data.all_data()
    maxPres = reg.max('pressure')
    minPres = reg.min('pressure')

    print('Max: '+str(maxPres))
    print('Min: '+str(minPres))

    print('ratio: '+str(minPres/maxPres))

    data.add_field(('gas', 'fracHI'), function=_HIfrac_chem, display_name="H I Mass fraction", units="")
    data.add_field(('gas', 'fracMgII'), function=_MgIIfrac_chem, display_name="Mg II Mass fraction", units="")
    data.add_field(('gas', 'fracCI'), function=_CIfrac_chem, display_name="C I Mass fraction", units="")
    data.add_field(('gas', 'fracCII'), function=_CIIfrac_chem, display_name="C II Mass fraction", units="")
    data.add_field(('gas', 'fracCIII'), function=_CIIIfrac_chem, display_name="C III Mass fraction", units="")
    data.add_field(('gas', 'fracCIV'), function=_CIVfrac_chem, display_name="C IV Mass fraction", units="")
    data.add_field(('gas', 'fracSiIII'), function=_SiIIIfrac_chem, display_name="Si III Mass fraction", units="")
    data.add_field(('gas', 'fracSiIV'), function=_SiIVfrac_chem, display_name="Si IV Mass fraction", units="")
    data.add_field(('gas', 'fracNV'), function=_NVfrac_chem, display_name="N V Mass fraction", units="")
    data.add_field(('gas', 'fracOVI'), function=_OVIfrac_chem, display_name="O VI Mass fraction", units="")
    data.add_field(('gas', 'fracNeVIII'), function=_NeVIIIfrac_chem, display_name="Ne VIII Mass fraction", units="")

    #p = yt.SlicePlot(data, 'z', 'temperature', origin='native')
    p = yt.SlicePlot(data, 'z', noChemField, origin = 'native')
    p.set_zlim(noChemField, 1e-4, 1.)
    #p = yt.ProjectionPlot(data, 'z', 'density')
    #p.set_zlim('densCIV', 1e1, 1e11)
    p.annotate_timestamp()
    p.save('../Chem_test/Chem_'+i+'_'+savedir+'.png')
