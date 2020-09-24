#definitions of mass fractions and ion densities
#for easy calling in other scripts without
#extensive lists of functions at the top of each scripts

import numpy as np
import trident as tri
import yt

atomFracs_tri = {'H': ['H_p0_density', 'H_p1_density'],
                'Mg': ['Mg_p0_density', 'Mg_p1_density', 'Mg_p2_density', 'Mg_p3_density', 'Mg_p4_density', 'Mg_p5_density', 'Mg_p6_density', 'Mg_p7_density', 'Mg_p8_density', 'Mg_p9_density', 'Mg_p10_density', 'Mg_p11_density', 'Mg_p12_density'],
                'C': ['C_p0_density', 'C_p1_density', 'C_p2_density', 'C_p3_density', 'C_p4_density', 'C_p5_density', 'C_p6_density'],
                'Si': ['Si_p0_density', 'Si_p1_density', 'Si_p2_density', 'Si_p3_density', 'Si_p4_density', 'Si_p5_density', 'Si_p6_density', 'Si_p7_density', 'Si_p8_density', 'Si_p9_density', 'Si_p10_density', 'Si_p11_density', 'Si_p12_density', 'Si_p13_density', 'Si_p14_density'],
                'N': ['N_p0_density', 'N_p1_density', 'N_p2_density', 'N_p3_density', 'N_p4_density', 'N_p5_density', 'N_p6_density', 'N_p7_density'],
                'O': ['O_p0_density', 'O_p1_density', 'O_p2_density', 'O_p3_density', 'O_p4_density', 'O_p5_density', 'O_p6_density', 'O_p7_density', 'O_p8_density'],
                'Ne': ['Ne_p0_density', 'Ne_p1_density', 'Ne_p2_density', 'Ne_p3_density', 'Ne_p4_density', 'Ne_p5_density', 'Ne_p6_density', 'Ne_p7_density', 'Ne_p8_density', 'Ne_p9_density', 'Ne_p10_density']}
atomFracs_chem = {'H': ['h   ', 'hp  '],
                'Mg': ['mg  ', 'mgp ', 'mg2p', 'mg3p', 'mg4p', 'mg5p'],
                'C': ['c   ', 'cp  ', 'c2p ', 'c3p ', 'c4p ', 'c5p ', 'c6p '],
                'Si': ['si  ', 'sip ', 'si2p', 'si3p', 'si4p', 'si5p'],
                'N': ['n   ', 'np  ', 'n2p ', 'n3p ', 'n4p ', 'n5p ', 'n6p ', 'n7p '],
                'O': ['o   ', 'op  ', 'o2p ', 'o3p ', 'o4p ', 'o5p ', 'o6p ', 'o7p ', 'o8p '],
                'Ne': ['ne  ', 'nep ', 'ne2p', 'ne3p', 'ne4p', 'ne5p', 'ne6p', 'ne7p', 'ne8p', 'ne9p'] }

atomFracs_chem_short = {'H': ['h', 'hp'],
                'Mg': ['mg', 'mgp', 'mg2p', 'mg3p', 'mg4p', 'mg5p'],
                'C': ['c', 'cp', 'c2p', 'c3p', 'c4p', 'c5p', 'c6p'],
                'Si': ['si', 'sip', 'si2p', 'si3p', 'si4p', 'si5p'],
                'N': ['n', 'np', 'n2p', 'n3p', 'n4p', 'n5p', 'n6p', 'n7p'],
                'O': ['o', 'op', 'o2p', 'o3p', 'o4p', 'o5p', 'o6p', 'o7p', 'o8p'],
                'Ne': ['ne', 'nep', 'ne2p', 'ne3p', 'ne4p', 'ne5p', 'ne6p', 'ne7p', 'ne8p', 'ne9p'] }

ionList = {"I": 0, "II": 1, "III": 2, "IV": 3, "V":4, "VI":5, "VII":6, "VIII":7, "IX":8, "X":9}

mp = 1.6727219e-24
masses = {"H":2,
            'Mg': 24,
            'C': 12,
            'Si': 28,
            'N': 14,
            'O': 16,
            'Ne': 20}


def addfield(data, atom, ion, fieldtype, datatype):
    #handle trident first
    if datatype == 'tri':
        data = addTridentField(data, atom, ion, fieldtype)
    #now chemistry
    elif datatype =='chem':
        data = addChemField(data, atom, ion, fieldtype)
    else:
        print("Unknown data type; use tri or chem")
    return data

def addTridentField(data, atom, ion, fieldtype):
    if fieldtype == 'frac':
        data = addTriFrac(data, atom, ion)
    elif fieldtype == 'dens':
        data = addTriDens(data, atom, ion)
    else:
        print("Unknown field type; use frac or dens")
    return data

def addChemField(data, atom, ion, fieldtype):
    if fieldtype == 'frac':
        data = addChemFrac(data, atom, ion)
    elif fieldtype == 'dens':
        data = addChemDens(data, atom, ion)
    else:
        print("Unknown field type; use frac or dens")
    return data

def addTriFrac(data, atom, ion):
    #add the atom
    tri.add_ion_fields(data, ions=[atom], ftype='gas')
    def _newFrac(field, data):
        fracList = atomFracs_tri[atom]
        botsum = np.sum([data[f] for f in fracList], axis=0)
        ionNum = ionList[ion]
        top = data[fracList[ionNum]]
        frac = top/data.apply_units(botsum, "g/cm**3")
        return frac
    data.add_field(('gas', 'frac'+atom+ion+'_tri'), function=_newFrac, display_name=atom+' '+ion+' Mass Fraction (Tri)', units="")
    return data

def addChemFrac(data, atom, ion):
    def _newFrac(field, data):
        try:
            fracList = atomFracs_chem[atom]
            botsum = np.sum([data[f] for f in fracList], axis=0)
            ionNum = ionList[ion]
            top = data[fracList[ionNum]]
            frac = top/botsum
        except(yt.utilities.exceptions.YTFieldNotFound):
            fracList = atomFracs_chem_short[atom]
            botsum = np.sum([data[f] for f in fracList], axis=0)
            ionNum = ionList[ion]
            top = data[fracList[ionNum]]
            frac = top/botsum
        return frac
    data.add_field(('gas', 'frac'+atom+ion+'_chem'), function=_newFrac, display_name=atom+' '+ion+' Mass Fraction', units="")
    return data

def addTriDens(data, atom, ion):
    #add the atom
    tri.add_ion_fields(data, ions=[atom], ftype='gas')
    def _newDens(field, data):
        fracList = atomFracs_tri[atom]
        ionNum = ionList[ion]
        fieldname = fracList[ionNum][:-7]+'number_density'
        return data[fieldname]
    data.add_field(('gas', 'dens'+atom+ion+'_tri'), function=_newDens, display_name=atom+' '+ion+' Number Density', units="1/cm**3")
    #trident already adds the number density! so you're all good here
    return data

def addChemDens(data, atom, ion):
    def _newDens(field, data):
        try:
            fracList = atomFracs_chem[atom]
            ionNum = ionList[ion]
            atomMass = masses[atom]
            top = data[(('flash', fracList[ionNum]))]
            frac = top*data['density']/data.apply_units((atomMass*mp), 'g')
        except(yt.utilities.exceptions.YTFieldNotFound):
            fracList = atomFracs_chem_short[atom]
            ionNum = ionList[ion]
            atomMass = masses[atom]
            top = data[(('flash', fracList[ionNum]))]
            frac = top*data['density']/data.apply_units((atomMass*mp), 'g')
        return frac
    data.add_field(('gas', 'dens'+atom+ion+'_chem'), function=_newDens, display_name=atom+' '+ion+' Number Density', units="1/cm**3")
    return data
