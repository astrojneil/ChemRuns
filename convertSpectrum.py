import numpy as np
c = 3e10 #cm/s
planckEV = 4.1357e-15
SFR = 50 #msun/yrs
tevo = 1e7 #yr  = 10 Myrs
Rstar = 5.5e-3*3.086e18 #cm

original = open('S1226-dereddened-SED.txt', 'r')
final = open('Spectrum_test.txt', 'w')
i = 0
firstline = "%6.4e %6.4e %6.4e \n"%(planckEV*c/(0.016), planckEV*c/(91.*1e-8), 1221)
final.write(firstline)
for line in original:
	ls = line.split()
	lam = float(ls[0])
	int_norm = float(ls[1])   #normalized intensity

	freq = c/(lam*1e-8) #convert lam from Ang to cm
	energy = freq*planckEV
	intens = int_norm*3.6e28   #un-normalized intensity

	Lout = intens*((SFR*tevo)/1e6)
	Bv = Lout*(lam**2/(c*1e8))*(1/(16*(np.pi**2)*(Rstar**2)))
	ln = "%6.4e %6.4e %6.4e \n"%(energy,freq,Bv)
	final.write(ln)
	i = i+1

print(lam)
print(i)
