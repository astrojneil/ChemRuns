import numpy as np
c = 3e10 #cm/s
planckEV = 4.1357e-15
SFR = 25 #msun/yrs
tevo = 1e7 #yr  = 10 Myrs
Rstar = 50*3.086e18 #cm

original = open('S1226-dereddened-SED.txt', 'r')
final = open('Spectrum_final.txt', 'w')
i = 0
firstline = "%6.4e %6.4e %6.4e \n"%(planckEV*c/(0.016), planckEV*c/(91.*1e-8), 1221)
final.write(firstline)
for line in original:
	ls = line.split()
	lam = float(ls[0])*1e-8
	int_norm = float(ls[1])

	freq = c/lam
        energy = freq*planckEV 
        intens = int_norm*3.6e28

	Lout = intens*((SFR*tevo)/1e6)
        Bv = Lout*(lam**2/c)*(1/(16*(np.pi**2)*(Rstar**2)))
	#maybe need to take out lam^2/c  as this likely converts ang to Hz, but John's spectrum is already Hz
        ln = "%6.4e %6.4e %6.4e \n"%(energy,freq,Bv)
	final.write(ln)
	i = i+1

print(lam)
print(i)
