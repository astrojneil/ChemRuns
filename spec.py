import yt
from yt.utilities.physical_constants import kboltz,mh
import numpy as np

def _hspec(field,data):
    return data['h   ']
yt.add_field("hspec",function=_hspec)
def _hpspec(field,data):
    return data['hp  ']
yt.add_field("hpspec",function=_hpspec)

def _hespec(field,data):
    return data['he  ']
yt.add_field("hespec",function=_hespec)
def _hepspec(field,data):
    return data['hep ']
yt.add_field("hepspec",function=_hepspec)
def _he2pspec(field,data):
    return data['he2p']
yt.add_field("he2pspec",function=_he2pspec)

def _cspec(field,data):
    return data['c   ']
yt.add_field("cspec",function=_cspec)
def _cpspec(field,data):
    return data['cp  ']
yt.add_field("cpspec",function=_cpspec)
def _c2pspec(field,data):
    return data['c2p ']
yt.add_field("c2pspec",function=_c2pspec)
def _c3pspec(field,data):
    return data['c3p ']
yt.add_field("c3pspec",function=_c3pspec)
def _c4pspec(field,data):
    return data['c4p ']
yt.add_field("c4pspec",function=_c4pspec)
def _c5pspec(field,data):
    return data['c5p ']
yt.add_field("c5pspec",function=_c5pspec)

def _nspec(field,data):
    return data['n   ']
yt.add_field("nspec",function=_nspec)
def _npspec(field,data):
    return data['np  ']
yt.add_field("npspec",function=_npspec)
def _n2pspec(field,data):
    return data['n2p ']
yt.add_field("n2pspec",function=_n2pspec)
def _n3pspec(field,data):
    return data['n3p ']
yt.add_field("n3pspec",function=_n3pspec)
def _n4pspec(field,data):
    return data['n4p ']
yt.add_field("n4pspec",function=_n4pspec)
def _n5pspec(field,data):
    return data['n5p ']
yt.add_field("n5pspec",function=_n5pspec)
def _n6pspec(field,data):
    return data['n6p ']
yt.add_field("n6pspec",function=_n6pspec)

def _ospec(field,data):
    return data['o   ']
yt.add_field("ospec",function=_ospec)
def _opspec(field,data):
    return data['op  ']
yt.add_field("opspec",function=_opspec)
def _o2pspec(field,data):
    return data['o2p ']
yt.add_field("o2pspec",function=_o2pspec)
def _o3pspec(field,data):
    return data['o3p ']
yt.add_field("o3pspec",function=_o3pspec)
def _o4pspec(field,data):
    return data['o4p ']
yt.add_field("o4pspec",function=_o4pspec)
def _o5pspec(field,data):
    return data['o5p ']
yt.add_field("o5pspec",function=_o5pspec)
def _o6pspec(field,data):
    return data['o6p ']
yt.add_field("o6pspec",function=_o6pspec)
def _o7pspec(field,data):
    return data['o7p ']
yt.add_field("o7pspec",function=_o7pspec)

def _nespec(field,data):
    return data['ne  ']
yt.add_field("nespec",function=_nespec)
def _nepspec(field,data):
    return data['nep ']
yt.add_field("nepspec",function=_nepspec)
def _ne2pspec(field,data):
    return data['ne2p']
yt.add_field("ne2pspec",function=_ne2pspec)
def _ne3pspec(field,data):
    return data['ne3p']
yt.add_field("ne3pspec",function=_ne3pspec)
def _ne4pspec(field,data):
    return data['ne4p']
yt.add_field("ne4pspec",function=_ne4pspec)
def _ne5pspec(field,data):
    return data['ne5p']
yt.add_field("ne5pspec",function=_ne5pspec)
def _ne6pspec(field,data):
    return data['ne6p']
yt.add_field("ne6pspec",function=_ne6pspec)
def _ne7pspec(field,data):
    return data['ne7p']
yt.add_field("ne7pspec",function=_ne7pspec)
def _ne8pspec(field,data):
    return data['ne8p']
yt.add_field("ne8pspec",function=_ne8pspec)
def _ne9pspec(field,data):
    return data['ne9p']
yt.add_field("ne9pspec",function=_ne9pspec)

def _naspec(field,data):
    return data['na  ']
yt.add_field("naspec",function=_naspec)
def _napspec(field,data):
    return data['nap ']
yt.add_field("napspec",function=_napspec)
def _na2pspec(field,data):
    return data['na2p']
yt.add_field("na2pspec",function=_na2pspec)

def _mgspec(field,data):
    return data['mg  ']
yt.add_field("mgspec",function=_mgspec)
def _mgpspec(field,data):
    return data['mgp ']
yt.add_field("mgpspec",function=_mgpspec)
def _mg2pspec(field,data):
    return data['mg2p']
yt.add_field("mg2pspec",function=_mg2pspec)
def _mg3pspec(field,data):
    return data['mg3p']
yt.add_field("mg3pspec",function=_mg3pspec)

def _sispec(field,data):
    return data['si  ']
yt.add_field("sispec",function=_sispec)
def _sipspec(field,data):
    return data['sip ']
yt.add_field("sipspec",function=_sipspec)
def _si2pspec(field,data):
    return data['si2p']
yt.add_field("si2pspec",function=_si2pspec)
def _si3pspec(field,data):
    return data['si3p']
yt.add_field("si3pspec",function=_si3pspec)
def _si4pspec(field,data):
    return data['si4p']
yt.add_field("si4pspec",function=_si4pspec)
def _si5pspec(field,data):
    return data['si5p']
yt.add_field("si5pspec",function=_si5pspec)

def _sspec(field,data):
    return data['s   ']
yt.add_field("sspec",function=_sspec)
def _spspec(field,data):
    return data['sp  ']
yt.add_field("spspec",function=_spspec)
def _s2pspec(field,data):
    return data['s2p ']
yt.add_field("s2pspec",function=_s2pspec)
def _s3pspec(field,data):
    return data['s3p ']
yt.add_field("s3pspec",function=_s3pspec)
def _s4pspec(field,data):
    return data['s4p ']
yt.add_field("s4pspec",function=_s4pspec)

def _caspec(field,data):
    return data['ca  ']
yt.add_field("caspec",function=_caspec)
def _capspec(field,data):
    return data['cap ']
yt.add_field("capspec",function=_capspec)
def _ca2pspec(field,data):
    return data['ca2p']
yt.add_field("ca2pspec",function=_ca2pspec)
def _ca3pspec(field,data):
    return data['ca3p']
yt.add_field("ca3pspec",function=_ca3pspec)
def _ca4pspec(field,data):
    return data['ca4p']
yt.add_field("ca4pspec",function=_ca4pspec)

def _fespec(field,data):
    return data['fe  ']
yt.add_field("fespec",function=_fespec)
def _fepspec(field,data):
    return data['fep ']
yt.add_field("fepspec",function=_fepspec)
def _fe2pspec(field,data):
    return data['fe2p']
yt.add_field("fe2pspec",function=_fe2pspec)
def _fe3pspec(field,data):
    return data['fe3p']
yt.add_field("fe3pspec",function=_fe3pspec)
def _fe4pspec(field,data):
    return data['fe4p']
yt.add_field("fe4pspec",function=_fe4pspec)

def _elecspec(field,data):
    return data['elec']
yt.add_field("elecspec",function=_elecspec)

def _myabar(field,data):
    term = (data['hspec']+data['hpspec'])/1.0
    term = term + (data['hespec']+data['hepspec']+data['he2pspec'])/4.0
    term = term + (data['cspec']+data['cpspec']+data['c2pspec']+data['c3pspec']+data['c4pspec']+data['c5pspec'])/12.0
    term = term + (data['nspec']+data['npspec']+data['n2pspec']+data['n3pspec']+data['n4pspec']+data['n5pspec']+data['n6pspec'])/14.0
    term = term + (data['ospec']+data['opspec']+data['o2pspec']+data['o3pspec']+data['o4pspec']+data['o5pspec']+data['o6pspec']+data['o7pspec'])/16.0
    term = term + (data['nespec']+data['nepspec']+data['ne2pspec']+data['ne3pspec']+data['ne4pspec']+data['ne5pspec']+data['ne6pspec']+data['ne7pspec']+data['ne8pspec']+data['ne9pspec'])/20.0
    term = term + (data['naspec']+data['napspec']+data['na2pspec'])/22.0
    term = term + (data['mgspec']+data['mgpspec']+data['mg2pspec']+data['mg3pspec'])/24.0
    term = term + (data['sispec']+data['sipspec']+data['si2pspec']+data['si3pspec']+data['si4pspec']+data['si5pspec'])/28.0
    term = term + (data['sspec']+data['spspec']+data['s2pspec']+data['s3pspec']+data['s4pspec'])/32.0
    term = term + (data['caspec']+data['capspec']+data['ca2pspec']+data['ca3pspec']+data['ca4pspec'])/40.0
    term = term + (data['fespec']+data['fepspec']+data['fe2pspec']+data['fe3pspec']+data['fe4pspec'])/52.0
    term = term + data['elecspec']/0.000549
    term = 1.0/term
    return term
yt.add_field("myabar",function=_myabar)

def _ndens(field,data):
    return data['dens']/(data['myabar']*mh)
yt.add_field("ndens",function=_ndens,units="cm**-3")

def _mysoundspeed(field,data):
    cs = 5./3.*kboltz*data['temp']/(mh*data['myabar'])
    cs = np.sqrt(cs)
    return cs
yt.add_field("mysoundspeed",function=_mysoundspeed)

def _mymachnumber(field,data):
    v2 = data['velx']**2 + data['vely']**2 + data['velz']**2
    v  = np.sqrt(v2)
    mn = v/data['mysoundspeed']
    return mn
yt.add_field("mymachnumber",function=_mymachnumber)

def _xvar(field,data):
    avgd = np.average(data['dens'])
    return np.log(data['dens']/avgd)
yt.add_field("xvar",function=_xvar)
