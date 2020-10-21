from openDatFile import FLASHdat_retrieve
import matplotlib.pyplot as plt
import numpy as np

cloudMass =1.223869564736320599e38


M1 = '../M1-v480-T1-chem/runfiles/CT.dat'
M6 = '../M6.2-v3000-T1-chem/runfiles/CT.dat'
M3 = '../M3.6-v3000-t3-chem/runfiles/CT.dat'

names = [M1, M3, M6]

for run in names:
    found90 = False
    found75 = False
    found50 = False

    print(run[3:-16])
    time = FLASHdat_retrieve(run, 'time/tcc')
    mass = FLASHdat_retrieve(run, 'mass_blob(>rho0/3.)')
    for i, m in enumerate(mass):
        if m < 0.9*cloudMass and not found90:
            found90 = True
            print("t90 = {:.2f} tcc".format(time[i]))
        if m < 0.75*cloudMass and not found75:
            found75 = True
            print("t75 = {:.2f} tcc".format(time[i]))
        if m < 0.5*cloudMass and not found50:
            found50 = True
            print("t50 = {:.2f} tcc".format(time[i]))
