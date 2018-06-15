# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 12:01:49 2017

@author: ebuieii
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
from pylab import *


rc('axes',linewidth=2.0)
mpl.rcParams['xtick.major.width']='0.75'
mpl.rcParams['xtick.minor.width']='0.75'
mpl.rcParams['ytick.major.width']='0.75'
mpl.rcParams['ytick.minor.width']='0.75'
mpl.rcParams['font.weight']='bold'
mpl.rcParams['axes.labelweight']='bold'

a = 16./14 #Oxygen/Nitrogen
b = 10**7.86/10**8.73 #abundance of nitrogen/oxygen
c = 16./28 #Oxygen/silicon
d = 10**7.52/10**8.73 #abundance of silicon/oxygen

c_h = 10**8.39/10**12
n_h = 10**7.86/10**12
o_h = 10**8.73/10**12
si_h = 10**7.52/10**12
mg_h = 10**7.54/10**12

IP = [[8.0e-2,8.0e-3,8.0e-4],[5.0e-2,5.0e-3,5.0e-4],[3.0e-2,3.0e-3,3.0e-4],[1.0e-2,1.0e-3,1.0e-4]]
turb = [10,30,45,60,80,100]
col_den = [1.858e+21,1.858e+20,1.858e+19,1.858e+18,1.858e+17] 
dens = [1.0e-23,1.0e-24,1.0e-25,1.0e-26,1.0e-27]

a10 = []; cloudy_Z03 = []
x1 = "/Figs/ISM_info_"
x2 = "/Volumes/bluehat02/" #Z03 data
x3 = "/Users/ebuieii/cloudy_Z03/"

def get_chem_value(file_with_path,var,var2,*kwargs):
    keys = np.array( ['Temp','H','H+','He','He+','He2+','C','C+','C2+','C3+','C4+','C5+','N','N+','N2+','N3+','N4+','N5+','N6+','O','O+','O2+','O3+','O4+','O5+','O6+','O7+','Ne','Ne+','Ne2+','Ne3+','Ne4+','Ne5+','Ne6+','Ne7+','Ne8+','Ne9+','Na','Na+','Na2+','Mg','Mg+','Mg2+','Mg3+','Si','Si+','Si2+','Si3+','Si4+','Si5+','So','S+','S2+','S3+','S4+','Ca','Ca+','Ca2+','Ca3+','Ca4+','Fe','Fe+','Fe2+','Fe3+','Fe4+'])
    kidx = np.array( [1,16,17,19,20,21,23,24,25,26,27,28,30,31,32,33,34,35,36,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,58,59,60,62,63,64,65,67,68,69,70,71,72,74,75,76,77,78,80,81,82,83,84,86,87,88,89,90])
    vark = np.array( ['Spec','MFrac','DW_Temp','DW_VD','Doppler','CIEX','<X(T)>','<T-X(T)>'] )
    
    idx = np.char.find(keys,var)
    try:
        idx = np.where(idx==0)[0][0]
    except IndexError:
        print "Error: Don't know what: %s is. I only know of: %s"%(var,keys)
        sys.exit()

    idx2 = np.char.find(vark,var2)
    try:
        idx2 = np.where(idx2==0)[0][0]
    except IndexError:
        print "Error: Don't know what: %s is. I only know of: %s"%(var,keys)
        sys.exit()
    fin = open(file_with_path,'r')
    for i in xrange(kidx[idx]):
        line = fin.readline()
    line = (line.strip()).split()
    value = float(line[idx2])
    return value

for i in range(3):
    for j in range(4):
        hydrogen = np.loadtxt(x3+'hydrogen_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2))
        helium = np.loadtxt(x3+'helium_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3))
        carbon = np.loadtxt(x3+'carbon_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5))
        nitrogen = np.loadtxt(x3+'nitrogen_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5,6,7,8))
        oxygen = np.loadtxt(x3+'oxygen_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5,6,7,8,9,10))
        neon = np.loadtxt(x3+'neon_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5,6,7,8,9))
        sodium = np.loadtxt(x3+'sodium_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3))
        magnesium = np.loadtxt(x3+'magnesium_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4))      
        silicon = np.loadtxt(x3+'silicon_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5,6,7,8,9,10))
        sulfur = np.loadtxt(x3+'sulphur_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5))
        calcium = np.loadtxt(x3+'calcium_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5))
        iron = np.loadtxt(x3+'iron_'+str(IP[j][0])[3]+'.0000e+0'+str(i+2)+'.col',skiprows=1,usecols=(1,2,3,4,5))
        cloudy_Z03.append((np.log10((silicon[3]/sum(silicon))/(oxygen[5]/sum(oxygen))*c*d),np.log10((nitrogen[4]/sum(nitrogen))/(oxygen[5]/sum(oxygen))*a*b)))

for i in range(3):
    for k in turb:
        for j in range(3):
            for m in range(4):                 
                    t = k
                    col = col_den[i]
                    den = dens[i]
                    ip = IP[m][j]
                    temp = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Temp','MFrac')
                    H1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','H','MFrac')
                    H2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','H+','MFrac')
                    He1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','He','MFrac')
                    He2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','He+','MFrac')
                    He3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','He2+','MFrac')
                    C1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C','MFrac')
                    C2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C+','MFrac')
                    C3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C2+','MFrac')
                    C4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C3+','MFrac')
                    C5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C4+','MFrac')
                    C6 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','C5+','MFrac')
                    N1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N','MFrac')
                    N2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N+','MFrac')
                    N3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N2+','MFrac')
                    N4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N3+','MFrac')
                    N5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N4+','MFrac')
                    N6 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N5+','MFrac')
                    N7 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','N6+','MFrac')
                    O1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O','MFrac')
                    O2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O+','MFrac')
                    O3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O2+','MFrac')
                    O4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O3+','MFrac')
                    O5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O4+','MFrac')
                    O6 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O5+','MFrac')
                    O7 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O6+','MFrac')
                    O8 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','O7+','MFrac')
                    Ne1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne','MFrac')
                    Ne2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne+','MFrac')
                    Ne3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne2+','MFrac')
                    Ne4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne3+','MFrac')
                    Ne5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne4+','MFrac')
                    Ne6 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne5+','MFrac')
                    Ne7 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne6+','MFrac')
                    Ne8 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne7+','MFrac')
                    Ne9 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne8+','MFrac')
                    Ne10 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ne9+','MFrac')
                    Na1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Na','MFrac')
                    Na2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Na+','MFrac')
                    Na3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Na2+','MFrac')
                    Mg1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Mg','MFrac')
                    Mg2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Mg+','MFrac')
                    Mg3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Mg2+','MFrac')
                    Mg4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Mg3+','MFrac')
                    Si1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si','MFrac')
                    Si2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si+','MFrac')
                    Si3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si2+','MFrac')
                    Si4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si3+','MFrac')
                    Si5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si4+','MFrac')
                    Si6 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Si5+','MFrac')
                    S1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','So','MFrac')
                    S2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','S+','MFrac')
                    S3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','S2+','MFrac')
                    S4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','S3+','MFrac')
                    S5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','S4+','MFrac')
                    Ca1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ca','MFrac')
                    Ca2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ca+','MFrac')
                    Ca3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ca2+','MFrac')
                    Ca4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ca3+','MFrac')
                    Ca5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Ca4+','MFrac')
                    Fe1 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Fe','MFrac')
                    Fe2 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Fe+','MFrac')
                    Fe3 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Fe2+','MFrac')
                    Fe4 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Fe3+','MFrac')
                    Fe5 = get_chem_value(x2+'1E2'+str(i+3)+'_S'+str(k)+x1+str(IP[m][0])[3]+'P0EM'+str(j+2)+'.dat','Fe4+','MFrac')                    
                    a10.append((np.log10(H1*col),np.log10(temp),np.log10(ip),np.log10(C2*col*c_h/12.0)))                   
"""
for the plotting, it starts at *3 and skips the first 2. The first 2 are the 2 lowest turbulence runs and we arent plotting that data for this first paper.
"""
ip1 = [item[2] for item in a10[0:12]]
o1 = [item[0] for item in a10[0:12]] #1e23_s10
o2 = [item[0] for item in a10[12:24]] #1e23_s30
o3 = [item[0] for item in a10[24:36]] #1e23_s45
o4 = [item[0] for item in a10[36:48]] #1e23_s60
o5 = [item[0] for item in a10[48:60]] #1e23_s80
o6 = [item[0] for item in a10[60:72]] #1e23_s100
o7 = [item[0] for item in a10[72:84]] #1e24_s10
o8 = [item[0] for item in a10[84:96]] #1e24_s30
o9 = [item[0] for item in a10[96:108]] #1e24_s45
o10 = [item[0] for item in a10[108:120]] #1e24_s60
o11 = [item[0] for item in a10[120:132]] #1e24_s80
o12 = [item[0] for item in a10[132:144]] #1e24_s100
o13 = [item[0] for item in a10[144:156]] #1e25_s10
o14 = [item[0] for item in a10[156:168]] #1e25_s30
o15 = [item[0] for item in a10[168:180]] #1e25_s45
o16 = [item[0] for item in a10[180:192]] #1e25_s60
o17 = [item[0] for item in a10[192:204]] #1e25_s80
o18 = [item[0] for item in a10[204:216]] #1e25_s100

b1 = [item[1] for item in a10[0:12]] #1e23_s10
b2 = [item[1] for item in a10[12:24]] #1e23_s30
b3 = [item[1] for item in a10[24:36]] #1e23_s45
b4 = [item[1] for item in a10[36:48]] #1e23_s60
b5 = [item[1] for item in a10[48:60]] #1e23_s80
b6 = [item[1] for item in a10[60:72]] #1e23_s100
b7 = [item[1] for item in a10[72:84]] #1e24_s10
b8 = [item[1] for item in a10[84:96]] #1e24_s30
b9 = [item[1] for item in a10[96:108]] #1e24_s45
b10 = [item[1] for item in a10[108:120]] #1e24_s60
b11 = [item[1] for item in a10[120:132]] #1e24_s80
b12 = [item[1] for item in a10[132:144]] #1e24_s100
b13 = [item[1] for item in a10[144:156]] #1e25_s10
b14 = [item[1] for item in a10[156:168]] #1e25_s30
b15 = [item[1] for item in a10[168:180]] #1e25_s45
b16 = [item[1] for item in a10[180:192]] #1e25_s60
b17 = [item[1] for item in a10[192:204]] #1e25_s80
b18 = [item[1] for item in a10[204:216]] #1e25_s100

c1 = [item[3] for item in a10[0:12]] #1e23_s10
c2 = [item[3] for item in a10[12:24]] #1e23_s30
c3 = [item[3] for item in a10[24:36]] #1e23_s45
c4 = [item[3] for item in a10[36:48]] #1e23_s60
c5 = [item[3] for item in a10[48:60]] #1e23_s80
c6 = [item[3] for item in a10[60:72]] #1e23_s100
c7 = [item[3] for item in a10[72:84]] #1e24_s10
c8 = [item[3] for item in a10[84:96]] #1e24_s30
c9 = [item[3] for item in a10[96:108]] #1e24_s45
c10 = [item[3] for item in a10[108:120]] #1e24_s60
c11 = [item[3] for item in a10[120:132]] #1e24_s80
c12 = [item[3] for item in a10[132:144]] #1e24_s100
c13 = [item[3] for item in a10[144:156]] #1e25_s10
c14 = [item[3] for item in a10[156:168]] #1e25_s30
c15 = [item[3] for item in a10[168:180]] #1e25_s45
c16 = [item[3] for item in a10[180:192]] #1e25_s60
c17 = [item[3] for item in a10[192:204]] #1e25_s80
c18 = [item[3] for item in a10[204:216]] #1e25_s100

x_broad = [-0.785092,-0.505453,-1.41201,-1.28388,-1.24761,-1.03807,-0.904322,-0.930573,-1.01158,-1.06290]#[-1.85,-1.41,-1.28,-1.25,-1.18,-1.11,-1.07,-1.06,-1.04,-1.01,-0.97,-0.95,-0.94,-0.92,-0.9, -0.85, -0.83, -0.8, -0.78, -0.73, -0.5, -0.42, -0.38, -0.28, -0.22, -0.2, 0.12] 
y_broad = [-1.79848,-0.942875,-1.36358,-1.48386,-1.44657,-1.37962,-1.41955,-1.68520,-1.54226,-1.07392]#[-2.18,-1.38,-1.48,-1.45,-1.49,-1.42,-1.9,-1.09,-1.39,-1.55,-1.27,-1.48,-1.11,-1.69,-1.42, -1.29, -1.25, -1.8, -1.07, -1.35, -0.95, -1.17, -0.56, -1.3, -0.68, -0.81, -0.31]
x_narrow = [-0.951664,-0.951845,-1.17757,0.124547,-0.833073,-1.07804,-0.733714,-0.206134,-0.381509,-0.935017,-0.414412]
y_narrow = [-1.47344,-1.47362,-1.48043,-0.312875,-1.25024,-1.88675,-1.33379,-0.806208,-0.557168,-1.11068,-1.16904]
x_nolos = [-1.11821,-0.961146,-0.282932,-0.845452,-0.225452,-1.83938,-0.772758]
y_nolos = [-1.42106,-1.26400,-1.29632,-1.28287,-0.662874,-2.16125,-1.06344]     

cloudy_so = [item[0] for item in cloudy_Z03]
cloudy_no = [item[1] for item in cloudy_Z03] 
  
#n3 = [item[4] for item in a10[24:36]] #1e23_s45
#n4 = [item[4] for item in a10[36:48]] #1e23_s60
#n5 = [item[4] for item in a10[48:60]] #1e23_s80
#n6 = [item[4] for item in a10[60:72]] #1e23_s100
#
#n9 = [item[4] for item in a10[96:108]] #1e24_s45
#n10 = [item[4] for item in a10[108:120]] #1e24_s60
#n11 = [item[4] for item in a10[120:132]] #1e24_s80
#n12 = [item[4] for item in a10[132:144]] #1e24_s100
#
#n15 = [item[4] for item in a10[168:180]] #1e25_s45
#n16 = [item[4] for item in a10[180:192]] #1e25_s60
#n17 = [item[4] for item in a10[192:204]] #1e25_s80
#n18 = [item[4] for item in a10[204:216]] #1e25_s100


axis_font = {'size':'40'}
fig_font = {'size':'25'}
#label_font = {'size':'20'}
s=90
"""
To get column density, multiply the mass fraction by the col and the relative solar abundance and divide by atomc mass for that element
also on comparison plot, black is N5, red is O6

also x/y stuff are points from werk 2016 Figure 12 data

for N5 column desity plots are from ylim([9,16]) and O6 column density plots are from ylim([8,17])
H1 column density plots are from ylim([14,21]), and make second term H1*col
temp plots have ylim([3.5,6.5]), and make first term temp
when x-axis is U, its from xlim([-4,-1.01]) for the first 3 and to -1 for the last one, plt.xticks(np.arange(-4,-1,1)) is to get the tick marks right for the first 3, -1 -> 0 for the last one
for N5/O6 ratio, ylim is from -2,0.5 on to row and -2,0.4 on bottom row
"""
plt.figure(1)




#This is how you plot W16 Figure 12 with data 

plt.subplot(221)
plt.scatter(x_broad,y_broad,c='g', edgecolors='None',s=s, label =r'$\rm \bf Broad$')
plt.scatter(x_narrow,y_narrow,c='orange', marker='v',edgecolors='None',s=s, label =r'$\rm \bf Narrow$')
plt.scatter(x_nolos,y_nolos,c='purple',marker='s',edgecolors='None',s=s, label =r'$\rm \bf No-low$')
plt.plot(b3, o3,'k--', linewidth=3, label =r'$\rm \bf N = 10^{21} \ cm^{-2}$') #10 km/s
plt.plot(b9, o9,'r-.', linewidth=3, label =r'$\rm \bf N = 10^{20} \ cm^{-2}$')
plt.plot(b15, o15,'b-', linewidth=3, label =r'$\rm \bf N = 10^{19} \ cm^{-2}$')
plt.plot(cloudy_no,cloudy_so,'c-', linewidth=3, label =r'$\rm \bf CLOUDY$')
plt.text(-1.8,-0.5,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=25)
plt.ylabel(r'$\rm \bf log \  N_{SiIV}/N_{OVI}$',**axis_font)
plt.gca().yaxis.set_label_coords(-.2,0)
plt.tick_params(axis='x',labelbottom='off')
plt.ylim([-3,0])
plt.xlim([-2,0.4])
plt.legend(loc='lower right',frameon=False,prop={'size': 20})


plt.subplot(222)
plt.plot(b4, o4,'k--', linewidth=3, label =r'$\rm \bf N = 10^{21} \ cm^{-2}$') #10 km/s
plt.plot(b10, o10,'r-.', linewidth=3, label =r'$\rm \bf N = 10^{20} \ cm^{-2}$')
plt.plot(b16, o16,'b-', linewidth=3, label =r'$\rm \bf N = 10^{19} \ cm^{-2}$')
plt.plot(cloudy_no,cloudy_so,'c-', linewidth=3, label =r'$\rm \bf CLOUDY$')
plt.scatter(x_broad,y_broad,c='g', edgecolors='None',s=s, label =r'$\rm \bf Broad$')
plt.scatter(x_narrow,y_narrow,c='orange', marker='v',edgecolors='None',s=s, label =r'$\rm \bf Narrow$')
plt.scatter(x_nolos,y_nolos,c='purple',marker='s',edgecolors='None',s=s, label =r'$\rm \bf No-low$')
plt.tick_params(axis='both', which='major', labelsize=25)
plt.text(-1.8,-0.5,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='x',labelbottom='off')
plt.ylim([-3,0])
plt.xlim([-2,0.5])
plt.gca().axes.yaxis.set_ticklabels([])


plt.subplot(223)
plt.plot(b5, o5,'k--', linewidth=3) #10 km/s
plt.plot(b11, o11,'r-.', linewidth=3)
plt.plot(b17, o17,'b-', linewidth=3)
plt.plot(cloudy_no,cloudy_so,'c-', linewidth=3)
plt.scatter(x_broad,y_broad,c='g',edgecolors='None',s=s)
plt.scatter(x_narrow,y_narrow,c='orange', marker='v',edgecolors='None',s=s)
plt.scatter(x_nolos,y_nolos,c='purple',marker='s',edgecolors='None',s=s)
plt.text(-1.8,-0.5,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=25)
plt.ylim([-3,-0.01])
plt.xlim([-2,0.4])
plt.xlabel(r'$\rm \bf log \ N_{NV}/N_{OVI}$', **axis_font)
plt.gca().xaxis.set_label_coords(1.0,-0.15)

plt.subplot(224)
plt.plot(b6, o6,'k--', linewidth=3) #10 km/s
plt.plot(b12, o12,'r-.', linewidth=3)
plt.plot(b18, o18,'b-', linewidth=3)
plt.plot(cloudy_no,cloudy_so,'c-', linewidth=3)
plt.scatter(x_broad,y_broad,c='g',edgecolors='None',s=s)
plt.scatter(x_narrow,y_narrow,c='orange', marker='v',edgecolors='None',s=s)
plt.scatter(x_nolos,y_nolos,c='purple',marker='s',edgecolors='None',s=s)
plt.text(-1.8,-0.5,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=25)
plt.ylim([-3,-0.01])
plt.xlim([-2,0.5])
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)
plt.show()
"""
#This is temp/HI plots

plt.subplot(241)
plt.plot(ip1, o3,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o9,'r-.', linewidth=3)
plt.plot(ip1, o15,'b-', linewidth=3)
plt.ylim([3.5,6.5])
plt.text(-3.8,6,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylabel(r'$\rm \bf log \  T \ [K]$',**axis_font)
plt.gca().yaxis.set_label_coords(-.25,0.5)
plt.tick_params(axis='x',labelbottom='off')
plt.xticks(np.arange(-4,-1,1))
plt.xlim([-4,-1.01])

plt.subplot(242)
plt.plot(ip1, o4,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o10,'r-.', linewidth=3)
plt.plot(ip1, o16,'b-', linewidth=3)
plt.ylim([3.5,6.5])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.text(-3.8,6,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.xlim([-4,-1.01])
plt.tick_params(axis='x',labelbottom='off')
plt.gca().axes.yaxis.set_ticklabels([])
plt.xticks(np.arange(-4,-1,1))

plt.subplot(243)
plt.plot(ip1, o5,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o11,'r-.', linewidth=3)
plt.plot(ip1, o17,'b-', linewidth=3)
plt.ylim([3.5,6.5])
plt.text(-3.8,6,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.gca().axes.yaxis.set_ticklabels([])
plt.xlim([-4,-1.01])
plt.tick_params(axis='x',labelbottom='off')
plt.xticks(np.arange(-4,-1,1))

plt.subplot(244)
plt.plot(ip1, o6,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o12,'r-.', linewidth=3)
plt.plot(ip1, o18,'b-', linewidth=3)
plt.ylim([3.5,6.5])
plt.text(-3.8,6,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlim([-4,-1])
plt.xticks(np.arange(-4,0,1))
plt.tick_params(axis='x',labelbottom='off')
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)

plt.subplot(245)
plt.plot(ip1, b3,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b9,'r-.', linewidth=3)
plt.plot(ip1, b15,'b-', linewidth=3)
plt.ylim([14,20.9])
plt.text(-3.0,20,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylabel(r'$\rm \bf log \  N_{HI} \ [cm^{-2}]$',**axis_font)
plt.gca().yaxis.set_label_coords(-.25,0.5)
plt.xticks(np.arange(-4,-1,1))
plt.xlim([-4,-1.01])

plt.subplot(246)
plt.plot(ip1, b4,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b10,'r-.', linewidth=3)
plt.plot(ip1, b16,'b-', linewidth=3)
plt.ylim([14,20.9])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.text(-3.0,20,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.xlim([-4,-1.01])
plt.gca().axes.yaxis.set_ticklabels([])
plt.xticks(np.arange(-4,-1,1))

plt.subplot(247)
plt.plot(ip1, b5,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b11,'r-.', linewidth=3)
plt.plot(ip1, b17,'b-', linewidth=3)
plt.ylim([14,20.9])
plt.text(-3.0,20,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.gca().axes.yaxis.set_ticklabels([])
plt.xlim([-4,-1.01])
plt.xticks(np.arange(-4,-1,1))
plt.xlabel(r'$\rm \bf log \ U$', **axis_font)
plt.gca().xaxis.set_label_coords(0,-0.15)

plt.subplot(248)
plt.plot(ip1, b6,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b12,'r-.', linewidth=3)
plt.plot(ip1, b18,'b-', linewidth=3)
plt.ylim([14,20.9])
plt.text(-3.0,20,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlim([-4,-1])
plt.xticks(np.arange(-4,0,1))
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)
plt.show()

Them NV column density, OVI column density and N5/O6 ratios right here fam

plt.subplot(341)
plt.plot(ip1, o3,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o9,'r-.', linewidth=3)
plt.plot(ip1, o15,'b-', linewidth=3)
plt.ylim([9,16])
plt.text(-3.8,15,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylabel(r'$\rm \bf log \ N_{NV} \ [cm^{-2}]$',**axis_font)
plt.gca().yaxis.set_label_coords(-.25,0.5)
plt.tick_params(axis='x',labelbottom='off')
plt.xticks(np.arange(-4,-1,1))
plt.xlim([-4,-1.01])

plt.subplot(342)
plt.plot(ip1, o4,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o10,'r-.', linewidth=3)
plt.plot(ip1, o16,'b-', linewidth=3)
plt.ylim([9,16])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.text(-3.8,15,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.xlim([-4,-1.01])
plt.tick_params(axis='x',labelbottom='off')
plt.gca().axes.yaxis.set_ticklabels([])
plt.xticks(np.arange(-4,-1,1))

plt.subplot(343)
plt.plot(ip1, o5,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o11,'r-.', linewidth=3)
plt.plot(ip1, o17,'b-', linewidth=3)
plt.ylim([9,16])
plt.text(-3.8,15,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.gca().axes.yaxis.set_ticklabels([])
plt.xlim([-4,-1.01])
plt.tick_params(axis='x',labelbottom='off')
plt.xticks(np.arange(-4,-1,1))

plt.subplot(344)
plt.plot(ip1, o6,'k--', linewidth=3) #10 km/s
plt.plot(ip1, o12,'r-.', linewidth=3)
plt.plot(ip1, o18,'b-', linewidth=3)
plt.ylim([9,16])
plt.text(-3.8,15,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlim([-4,-1])
plt.xticks(np.arange(-4,0,1))
plt.tick_params(axis='x',labelbottom='off')
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)

plt.subplot(345)
plt.plot(ip1, b3,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b9,'r-.', linewidth=3)
plt.plot(ip1, b15,'b-', linewidth=3)
plt.ylim([8,16.9])
plt.text(-3.8,16,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylabel(r'$\rm \bf log \  N_{OVI} \ [cm^{-2}]$',**axis_font)
plt.gca().yaxis.set_label_coords(-.25,0.5)
plt.xticks(np.arange(-4,-1,1))
plt.tick_params(axis='x',labelbottom='off')
plt.xlim([-4,-1.01])

plt.subplot(346)
plt.plot(ip1, b4,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b10,'r-.', linewidth=3)
plt.plot(ip1, b16,'b-', linewidth=3)
plt.ylim([8,16.9])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.text(-3.8,16,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.xlim([-4,-1.01])
plt.gca().axes.yaxis.set_ticklabels([])
plt.tick_params(axis='x',labelbottom='off')
plt.xticks(np.arange(-4,-1,1))

plt.subplot(347)
plt.plot(ip1, b5,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b11,'r-.', linewidth=3)
plt.plot(ip1, b17,'b-', linewidth=3)
plt.ylim([8,16.9])
plt.text(-3.8,16,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.gca().axes.yaxis.set_ticklabels([])
plt.tick_params(axis='x',labelbottom='off')
plt.xlim([-4,-1.01])
plt.xticks(np.arange(-4,-1,1))

plt.subplot(348)
plt.plot(ip1, b6,'k--', linewidth=3) #10 km/s
plt.plot(ip1, b12,'r-.', linewidth=3)
plt.plot(ip1, b18,'b-', linewidth=3)
plt.ylim([8,16.9])
plt.text(-3.8,16,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlim([-4,-1])
plt.xticks(np.arange(-4,0,1))
plt.tick_params(axis='x',labelbottom='off')
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)

plt.subplot(349)
plt.plot(ip1, c3,'k--', linewidth=3) #10 km/s
plt.plot(ip1, c9,'r-.', linewidth=3)
plt.plot(ip1, c15,'b-', linewidth=3)
plt.ylim([-2,0.49])
plt.text(-3.8,-1.5,r'$\rm \bf \sigma_{1D} = 26 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylabel(r'$\rm \bf log \  N_{NV}/N_{OVI}$',**axis_font)
plt.gca().yaxis.set_label_coords(-.25,0.5)
plt.xticks(np.arange(-4,-1,1))
plt.xlim([-4,-1.01])

plt.subplot(3,4,10)
plt.plot(ip1, c4,'k--', linewidth=3) #10 km/s
plt.plot(ip1, c10,'r-.', linewidth=3)
plt.plot(ip1, c16,'b-', linewidth=3)
plt.ylim([-2,0.49])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.text(-3.8,-1.5,r'$\rm \bf \sigma_{1D} = 35 \ km \ s^{-1}$',**fig_font)
plt.xlim([-4,-1.01])
plt.gca().axes.yaxis.set_ticklabels([])
plt.xticks(np.arange(-4,-1,1))

plt.subplot(3,4,11)
plt.plot(ip1, c5,'k--', linewidth=3) #10 km/s
plt.plot(ip1, c11,'r-.', linewidth=3)
plt.plot(ip1, c17,'b-', linewidth=3)
plt.ylim([-2,0.49])
plt.text(-3.8,-1.5,r'$\rm \bf \sigma_{1D} = 46 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.gca().axes.yaxis.set_ticklabels([])
plt.xlim([-4,-1.01])
plt.xlabel(r'$\rm \bf Ionization \ Parameter \ log \ U$', **axis_font)
plt.gca().xaxis.set_label_coords(0,-0.15)
plt.xticks(np.arange(-4,-1,1))

plt.subplot(3,4,12)
plt.plot(ip1, c6,'k--', linewidth=3) #10 km/s
plt.plot(ip1, c12,'r-.', linewidth=3)
plt.plot(ip1, c18,'b-', linewidth=3)
plt.ylim([-2,0.49])
plt.text(-3.8,-1.5,r'$\rm \bf \sigma_{1D} = 58 \ km \ s^{-1}$',**fig_font)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlim([-4,-1])
plt.xticks(np.arange(-4,0,1))
plt.gca().axes.yaxis.set_ticklabels([])
plt.subplots_adjust(hspace=0, wspace=0)
plt.show()

"""
