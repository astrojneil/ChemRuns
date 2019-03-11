sim_xH    = 1.2341e-5
sim_xHP   = 7.0522e-1
sim_xHE   = 2.1410e-5
sim_xHEP  = 3.3569e-2
sim_xHE2P = 2.4852e-1
sim_xC    = 2.5502e-8
sim_xCP   = 3.5455e-5
sim_xC2P  = 1.2627e-3
sim_xC3P  = 5.8262e-4
sim_xC4P  = 1.9241e-4
sim_xC5P  = 0.0000e0
sim_xN    = 2.5206e-8
sim_xNP   = 2.9911e-5
sim_xN2P  = 4.8648e-4
sim_xN3P  = 3.2180e-4
sim_xN4P  = 1.7896e-6
sim_xN5P  = 6.0550e-9
sim_xN6P  = 0.0000e0
sim_xO    = 1.5647e-7
sim_xOP   = 1.9850e-4
sim_xO2P  = 3.6400e-3
sim_xO3P  = 1.6863e-3
sim_xO4P  = 8.0723e-6
sim_xO5P  = 0.0000e0
sim_xO6P  = 0.0000e0
sim_xO7P  = 0.0000e0
sim_xNE   = 7.5460e-8
sim_xNEP  = 1.2313e-4
sim_xNE2P = 1.0127e-3
sim_xNE3P = 2.7363e-4
sim_xNE4P = 1.1778e-6
sim_xNE5P = 0.0000e0
sim_xNE6P = 0.0000e0
sim_xNE7P = 0.0000e0
sim_xNE8P = 0.0000e0
sim_xNE9P = 0.0000e0
sim_xNA   = 2.211e-12
sim_xNAP  = 1.3310e-6
sim_xNA2P = 3.1880e-5
sim_xMG   = 0.0000e0
sim_xMGP  = 3.6296e-8
sim_xMG2P = 4.8864e-4
sim_xMG3P = 9.8798e-5
sim_xSI   = 0.0000e0
sim_xSIP  = 1.5074e-7
sim_xSI2P = 2.2132e-5
sim_xSI3P = 8.1539e-5
sim_xSI4P = 5.8173e-4
sim_xSI5P = 0.0000e0
sim_xS    = 0.0000e0
sim_xSP   = 2.1967e-6
sim_xS2P  = 1.0339e-4
sim_xS3P  = 2.3710e-4
sim_xS4P  = 7.2667e-5
sim_xCA   = 0.0000e0
sim_xCAP  = 1.4858e-7
sim_xCA2P = 3.8113e-5
sim_xCA3P = 2.5064e-5
sim_xCA4P = 1.2569e-6
sim_xFE   = 0.0000e0
sim_xFEP  = 5.1630e-8
sim_xFE2P = 2.2262e-5
sim_xFE3P = 4.5882e-4
sim_xFE4P = 5.6469e-4
sim_xELEC = 6.4889e-4

sumh = sim_xH+sim_xHP
total = sim_xHE+sim_xHEP+sim_xHE2P+sim_xC+sim_xCP+sim_xC2P+sim_xC3P+sim_xC4P+sim_xC5P+sim_xN+sim_xNP+sim_xN2P+sim_xN3P+sim_xN4P+sim_xN5P+sim_xN6P+sim_xO+sim_xOP+sim_xO2P+sim_xO3P+sim_xO4P+sim_xO5P+sim_xO6P+sim_xO7P+sim_xNE+sim_xNEP+sim_xNE2P+sim_xNE3P+sim_xNE4P+sim_xNE5P+sim_xNE6P+sim_xNE7P+sim_xNE8P+sim_xNE9P+sim_xNA+sim_xNAP+sim_xNA2P+sim_xMG+sim_xMGP+sim_xMG2P+sim_xMG3P+sim_xSI+sim_xSIP+sim_xSI2P+sim_xSI3P+sim_xSI4P+sim_xSI5P+sim_xS+sim_xSP+sim_xS2P+sim_xS3P+sim_xS4P+sim_xCA+sim_xCAP+sim_xCA2P+sim_xCA3P+sim_xCA4P+sim_xFE+sim_xFEP+sim_xFE2P+sim_xFE3P+sim_xFE4P

sumall = 1.-total

if( abs(sumh-sumall) > 1.0e-5):
    sim_xH = sim_xH  * (sumall/sumh)
    sim_xHP = sim_xHP * (sumall/sumh)

sim_xELEC = (0.000549)*(sim_xHP/1.0 + sim_xHEP/4.0 + 2.0*sim_xHE2P/4.0)

total = sim_xH+sim_xHP+sim_xHE+sim_xHEP+sim_xHE2P+sim_xC+sim_xCP+sim_xC2P+sim_xC3P+sim_xC4P+sim_xC5P+sim_xN+sim_xNP+sim_xN2P+sim_xN3P+sim_xN4P+sim_xN5P+sim_xN6P+sim_xO+sim_xOP+sim_xO2P+sim_xO3P+sim_xO4P+sim_xO5P+sim_xO6P+sim_xO7P+sim_xNE+sim_xNEP+sim_xNE2P+sim_xNE3P+sim_xNE4P+sim_xNE5P+sim_xNE6P+sim_xNE7P+sim_xNE8P+sim_xNE9P+sim_xNA+sim_xNAP+sim_xNA2P+sim_xMG+sim_xMGP+sim_xMG2P+sim_xMG3P+sim_xSI+sim_xSIP+sim_xSI2P+sim_xSI3P+sim_xSI4P+sim_xSI5P+sim_xS+sim_xSP+sim_xS2P+sim_xS3P+sim_xS4P+sim_xCA+sim_xCAP+sim_xCA2P+sim_xCA3P+sim_xCA4P+sim_xFE+sim_xFEP+sim_xFE2P+sim_xFE3P+sim_xFE4P

H_tot = sim_xH+sim_xHP
He_tot = sim_xHE+sim_xHEP+sim_xHE2P
C_tot = sim_xC+sim_xCP+sim_xC2P+sim_xC3P+sim_xC4P+sim_xC5P
N_tot = sim_xN+sim_xNP+sim_xN2P+sim_xN3P+sim_xN4P+sim_xN5P+sim_xN6P
O_tot = sim_xO+sim_xOP+sim_xO2P+sim_xO3P+sim_xO4P+sim_xO5P+sim_xO6P+sim_xO7P
Ne_tot = sim_xNE+sim_xNEP+sim_xNE2P+sim_xNE3P+sim_xNE4P+sim_xNE5P+sim_xNE6P+sim_xNE7P+sim_xNE8P+sim_xNE9P
Na_tot = sim_xNA+sim_xNAP+sim_xNA2P
Mg_tot = sim_xMG+sim_xMGP+sim_xMG2P+sim_xMG3P
Si_tot = sim_xSI+sim_xSIP+sim_xSI2P+sim_xSI3P+sim_xSI4P+sim_xSI5P
S_tot = sim_xS+sim_xSP+sim_xS2P+sim_xS3P+sim_xS4P
Ca_tot = sim_xCA+sim_xCAP+sim_xCA2P+sim_xCA3P+sim_xCA4P
Fe_tot = sim_xFE+sim_xFEP+sim_xFE2P+sim_xFE3P+sim_xFE4P
ele_tot = sim_xELEC

print(total)

print('H: '+str(H_tot/total))
print('He: '+str(He_tot/total))
print('C: '+str(C_tot/total))
print('N: '+str(N_tot/total))
print('O: '+str(O_tot/total))
print('Ne: '+str(Ne_tot/total))
print('Na: '+str(Na_tot/total))
print('Mg: '+str(Mg_tot/total))
print('Si: '+str(Si_tot/total))
print('S: '+str(S_tot/total))
print('Ca: '+str(Ca_tot/total))
print('Fe: '+str(Fe_tot/total))
print('elec: '+str(ele_tot/total))
