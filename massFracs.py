#definitions of mass fractions and ion densities
#for easy calling in other scripts without
#extensive lists of functions at the top of each scripts

import numpy as np
import trident as trident
import yt

atomFracs_tri = {'H': ['H_p0_density', 'H_p1_density']}
atomFracs_chem = {'H': ['h    ', 'hp   '}
ionList = {"I": 0, "II": 1, "III": 2, "IV": 3, "V":4, "VI":5, "VII":6, "VIII":7, "IX":8, "X":9}
mp = 1.6727219e-24
masses = {"H":2}


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
        botsum = np.sum([data[f] for f in fracList])
        ionNum = ionList[ion]
        top = data[fracList[ionNum]]
        frac = top/botsum
        return dens
    data.add_field(('gas', 'frac'+atom+ion+'_tri'), function=_newFrac, display=atom+' '+ion+' Mass Fraction (Tri)', units="")
    return data

def addChemFrac(data, atom, ion):
    def _newFrac(field, data):
        fracList = atomFracs_chem[atom]
        botsum = np.sum([data[f] for f in fracList])
        ionNum = ionList[ion]
        top = data[fracList[ionNum]]
        frac = top/botsum
        return dens
    data.add_field(('gas', 'frac'+atom+ion+'_chem'), function=_newFrac, display=atom+' '+ion+' Mass Fraction', units="")
    return data

def addTriDens(data, atom, field):
    #add the atom
    tri.add_ion_fields(data, ions=[atom], ftype='gas')
    def _newDens(field, data):
        fracList = atomFracs_tri[atom]
        ionNum = ionList[ion]
        fieldname = fracList[ionNum][:-7]+'number_density'
        return data[fieldname]
    data.add_field(('gas, dens'+atom+ion+'_tri'), function=_newDens, display=atom+' '+ion+' Number Density', units='cm^-3')
    #trident already adds the number density! so you're all good here
    return data

def addChemDens(data, atom, field):
    def _newDens(field, data):
        fracList = atomFracs_chem[atom]
        ionNum = ionList[ion]
        atomMass = masses[atom]
        top = data[fracList[ionNum]]
        frac = top*data['density']/(atomMass*mp)
        return dens
    data.add_field(('gas', 'dens'+atom+ion+'_chem'), function=_newDens, display=atom+' '+ion+' Number Density', units="cm^-3")
    return data
