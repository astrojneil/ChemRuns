#read ascii file from Starburst99 and convert it to a Spectrum.txt file
import numpy as np

c = 3e10 #cm/s
planckEV = 4.1357e-15
readfile = open('S1226.ascii', 'r')
SFR = 25 #msun/yrs
tevo = 1e7 #yr  = 10 Myrs 
Rstar = 50*3.086e18 #cm

#loop through read file lines
i = 0
j=0
#array of values; first is wavelengths, next are fluxes at times
values  = []
for item in range(13):
    values.append([])
storeArray = values[j]

for line in readfile:
    #skip header of readfile
    if i > 12:
        #read each line's values
        ls = line.split()
        #read rows until end of each block
        if len(ls) > 1:
            for v in ls:
                storeArray.append(float(v))
        #if at the end of the block
        else:
            #add last value
            storeArray.append(float(ls[0]))
            #change storage array
            j = j+1
            storeArray = values[j]
    i = i+1
readfile.close()

for time in range(len(values)-2):
    writefile = open('Ascii_Spectrum_time'+str(time+1)+'.txt', 'w')
    writefile.write("%6.4e %6.4e %6.4e \n"%(planckEV*c/(values[0][-1]*1e-8), planckEV*c/(values[0][0]*1e-8), len(values[0])))
    for r in range(len(values[0])):
	p = -1 - r
	convert99 = 10**(np.log10(values[time+1][p]) + 44.077911)
	Lout = convert99*((SFR*tevo)/1e6)
	lam = values[0][p]*1e-8 #cm
	Bv = Lout*(lam**2/c)*(1/(16*(np.pi**2)*(Rstar**2)))
        
	freq = c/(values[0][p]*1e-8) 
        energy = freq*planckEV 
        intes = Bv
        ln = "%6.4e %6.4e %6.4e \n"%(energy,freq,intes)
	writefile.write(ln)
    writefile.close()
