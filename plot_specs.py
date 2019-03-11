import matplotlib.pyplot as plt
import numpy as np

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


spec1 = read_file('Spectrum_mine.txt')
spec2 = read_file('Ascii_Spectrum_time1.txt')
spec3 = read_file('Ascii_Spectrum_time6.txt')
spec4 = read_file('Ascii_Spectrum_time11.txt')
spec5 = read_file('Spectrum_HM0.txt')

plt.plot(spec1[0], spec1[2], label='mine')
plt.plot(spec2[0], spec2[2], label='time1')
plt.plot(spec3[0], spec3[2], label='time6')
plt.plot(spec4[0], spec4[2], label='time11')
plt.plot(spec5[0], spec5[2], label='HM0')
plt.legend(loc=2)

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy')
plt.ylabel('Intensity')

fig = plt.gcf()
fig.savefig('test.png')
