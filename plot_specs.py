import matplotlib.pyplot as plt
import numpy as np
h = 4.1357e-15
c_sp = 3e10


def read_file(filename):
    f = open(filename, 'r')
    en = []
    fre = []
    intens = []
    i = 0
    for line in f:
        if i > 0:
            ls = line.split()
            en.append(float(ls[0]))
            fre.append(float(ls[1]))
            intens.append(float(ls[2]))
        i = i+1

    en = np.array(en)
    fre = np.array(fre)
    intens = np.array(intens)
    return [en, fre, intens]

def read_file2(filename):
    f = open(filename, 'r')
    en = []
    fre = []
    intens = []
    i = 0
    for line in f:
        if i > 1:
            ls = line.split()
            en.append(float(ls[0])*13.605698066)
            intens.append(float(ls[1]))
        i = i+1

    en = np.array(en)
    intens = np.array(intens)
    intens_new = ((h*c_sp/en)**2)/(4*np.pi*c_sp)*intens
    return [en, intens_new]


spec1 = read_file('Spectrum_test.txt')
spec2 = read_file('Spectrum_cloudy.txt')


plt.plot(spec1[0], spec1[2], label='John Spec Converted')
plt.plot(spec2[0], spec2[2], label='Cloudy Spec Converted')
plt.legend(loc=2)

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy')
plt.ylabel('Intensity')

fig = plt.gcf()
fig.savefig('test.png')
