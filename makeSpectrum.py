import numpy as np
import sys

RydToeV  = 13.6           #eV
planckeV = 4.135667e-15   #eV * s 
speedOfLight = 3.0e10     #cm/s
boltzmannConst = 8.617e-5 #eV/K
eVtoerg        = 1.60218e-12 

def makeBlackBody(factor):
	nvals  = 10000
	eStart = 1.0e-8
	eEnd   = 1.0e8
	Temp   = factor
	if(Temp < 1000):
		print("Bad factor in BlackBody spectrum")
		print("I got: %6.4e but that seems low to me!"%(Temp))
		sys.exit("Bad Factor")
	if(Temp > 1.0e6):
		print("Bad factor in BlackBody spectrum")
		print("I got: %6.4e but that seems high to me!"%(Temp))
		sys.exit("Bad Factor")
	energy = np.logspace(np.log10(eStart),np.log10(eEnd),num=nvals,endpoint=True)
	freq   = energy/planckeV
	topPart = (2.0*planckeV*eVtoerg*freq*freq*freq)/(speedOfLight*speedOfLight)
	botPart = (planckeV*freq)/(boltzmannConst*Temp)
	Inten = np.where(botPart > 100, 1.0e-100, topPart/(np.exp(botPart)-1.0))
	fileout = open("Spectrum.txt","w")
	ln = "%6.4e %6.4e %6.4e\n"%(eStart,eEnd,nvals)
	fileout.write(ln)
	for i in range(len(energy)):
		ln = "%6.4e %6.4e %6.4e \n"%(energy[i],freq[i],Inten[i])
		fileout.write(ln)

def makeHM(factor):
	redshift = factor
	HMdata = np.loadtxt('UVB.txt')
	redshifts = HMdata[0,1:]

	if(factor < redshifts[0]):
		print("Bad factor in HM spectrum")
		print("I got: %6.4e but lowest is %6.4e"%(factor,redshifts[0]))
		sys.exit("Bad Factor")
	if(factor > redshifts[len(redshifts)-1]):
		print("Bad factor in HM spectrum")
		print("I got: %6.4e but highest is %6.4e"%(factor,redshifts[len(redshifts)-1]))
		sys.exit("Bad Factor")

	wavelengths = HMdata[1:,0] #In Units Angstroms
	for i in range( len(wavelengths)-1):
		if(wavelengths[i] == wavelengths[i+1]):
			wavelengths[i+1] = wavelengths[i] + (wavelengths[i+2]-wavelengths[i])/2.
	backgrounds = HMdata[1:,1:]
	#Now interpolate for the given redshift
	for i in range(len(redshifts)-1):
		if( redshift >= redshifts[i] and redshift < redshifts[i+1]):
			indx = i
			break
	wantedIntensities = np.zeros(len(backgrounds[:,0]))
	interpTerm = (redshift-redshifts[indx])/(redshifts[indx+1]-redshifts[indx])
	wantedIntensities = backgrounds[:,indx] + (backgrounds[:,indx+1]-backgrounds[:,indx])*interpTerm
	energy  = planckeV*speedOfLight/(wavelengths*1.0e-8)
	freq    = energy/planckeV
	fileout = open("Spectrum.txt","w")
	eStart  = energy[0]
	eEnd    = energy[len(energy)-1]
	nvals   = len(energy)
	ln = "%6.4e %6.4e %6.4e\n"%(eEnd,eStart,nvals)
	fileout.write(ln)
	for i in range(len(energy)):
		ii = len(energy)-1-i
		ln = "%6.4e %6.4e %6.4e \n"%(energy[ii],freq[ii],wantedIntensities[ii])
		fileout.write(ln)

def makeMRPowerLaw(factor):
	nvals = 1000
	eStart =1.0e-8
	eEnd   =1.0e8

	energy = np.logspace(np.log10(eStart),np.log10(eEnd),num=nvals,endpoint=True)
	freq   = energy/planckeV
	inten  = np.zeros(nvals)
	for i in range(nvals):
		if(energy[i] < 13.6):
			inten[i] = np.power(energy[i],-1.0)
		elif(energy[i]>500.0):
			inten[i] = 0.05*np.power(energy[i],-0.8)
		else:
			inten[i] = 3.8*np.power(energy[i],-1.5)
	fileout=open("Spectrum.txt","w")
	ln="%6.4e %6.4e %6.4e \n"%(eStart,eEnd,nvals)
	fileout.write(ln)
	for i in range(nvals):
		ln = "%6.4e %6.4e %6.4e \n"%(energy[i],freq[i],inten[i])
		fileout.write(ln)




def main():
	nparams = len(sys.argv)
	if(nparams != 3):
		print("Not enough parameters to makeSpectrum.py")
		print("Usage: python makeSpectrum.py SpectralShape Factor")
		print("SpectralShape can be BlackBody or HM or Powerlaw")
		print("Factor: For Blackbody defines the Temperature")
		print("For HM defines Redshift")
		print("For Powerlaw just put zero")
		sys.exit("Not enough parameters to makeSpectrum.py")
	else:
		specShape  = str(sys.argv[1])
		specFactor = float(sys.argv[2])
		print("specShape is: %s"%specShape)
		print("specFactor is: %6.4e"%(specFactor))

	if(specShape == "BlackBody"):
		makeBlackBody(specFactor)
	elif(specShape == "HM"):
		makeHM(specFactor)
	elif(specShape == "Powerlaw"):
		makeMRPowerLaw(specFactor)
	else:
		print("I don't know what shape you want.")
		print("Got: %s, but I only know BlackBody or HM"%(specShape))
		sys.exit("Unknown specShape")



if __name__ == '__main__':
	main()
