#read ascii file from Starburst99 and convert it to a Spectrum.txt file
import numpy as np

c = 3e10 #cm/s
planckEV = 4.1357e-15
readfile = open('S1226.ascii', 'r')
#writefile = open('Ascii_Spectrum.txt', 'w')

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
    writefile.write("%6.4e %6.4e %6.4e \n"%(c/(values[0][-1]*1e-8), c/(values[0][0]*1e-8), len(values[0])))
    for r in range(len(values[0])):
	p = -1 - r
        freq = c/(values[0][p]*1e-8) 
        energy = freq*planckEV 
        intes = values[time+1][p]
        ln = "%6.4e %6.4e %6.4e \n"%(energy,freq,intes)
	writefile.write(ln)
    writefile.close()
