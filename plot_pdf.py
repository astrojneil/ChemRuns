import yt
yt.funcs.mylog.setLevel(50)
from yt.mods import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy
import scipy.stats
import sys
from spec import *
import glob
import h5py
import subprocess

kboltz = 1.38065e-16
mh = 1.67262e-24

def get_ion(ip_value):
    fvalues = np.array([0.0, 1.0e-4, 3.0e-4, 5.0e-4, 8.0e-4, 1.0e-3, 3.0e-3, 5.0e-3, 8.0e-3, 1.0e-2, 3.0e-2, 5.0e-2, 8.0e-2, 1.0e-1])
    fnames  = np.array(['ZERO','A','B','C','D','E','F','G','H','I','J','K','L','M'])

    idx = np.argmin(np.abs(fvalues-ip_value))
    ipstr = fnames[idx]
    ln = '/Volumes/GiantDrive1/ChemRuns/fpys/ionization_state_%s.dat'%(ipstr)
#ln = '/p/lscratchd/gray58/TurbTest/3E26_S60/ionization_state_%s.dat'%(ipstr)
#ln = '/Volumes/Mirror1-8TB/wgray/fpys/ionization_state_%s.dat'%(ipstr)
    print 'OPENING: ',ln
    data = np.loadtxt(ln)
    data = np.where(data < 1.0e-30, 1.0e-30, data)
    return data,ipstr

def get_uvfiles(dire):
    data =  np.loadtxt(dire+'KH.dat',skiprows=1)
    nlines,nvars = data.shape

    #open all files
    files = glob.glob(dire+'KH_hdf5_chk_*')
    files.sort()
    ftimes=[]
    den = 1.
    ids = np.zeros(len(files))
    cj21s = np.zeros(len(files))
    times = np.zeros(len(files))
    nhtots = np.zeros(len(files))
    IP_Vs = np.zeros(len(files))

    for i in xrange(len(files)):
        print 'TRYING TO LOAD: ', files[i]
        pf = yt.load(files[i])
        ftimes.append(float(pf.current_time))

    for i in xrange(nlines-1):
        time = data[i,0]
        idx = np.argmin(np.abs(time-ftimes))  #find file index that line i is closest to
        if(time-ftimes[idx]==0.):   #are you at the line that corresponds to the file?
            ids[idx] = i
            cj21s[idx] = data[i,222]
            times[idx] = time
            nhtots[idx] = (data[i,23]+data[i,24])*den/mh
            IP_Vs[idx] = cj21s[idx] * 4.1735e-5 / nhtots[idx]
    '''
    #add last data point
	#id.append(nlines-2)
	#cj21.append(data[nlines-2,222]) #flux
	#time.append(data[nlines-2,0]) #time
	#nhtot.append( (data[nlines-2,23]+data[nlines-2,24])*den / mh ) #h fractions - need new indices
	#IP_V.append( cj21[-1]*4.1735e-5 / nhtot[-1] )  #needs nhtot


	rfiles = []
	time = np.array(time)
	ftimes = np.array(ftimes)
    IP = []
	IPName = []
    #fvalues is ionization parameter, should match a list in flash.par
    	fvalues = np.array([0.0, 1.0e-4, 3.0e-4, 5.0e-4, 8.0e-4, 1.0e-3, 3.0e-3, 5.0e-3, 8.0e-3, 1.0e-2, 3.0e-2, 5.0e-2, 8.0e-2, 1.0e-1])
    #names of the list - names the data files according to the ionization parameter
    	fnames  = np.array(['ZERO','1P0EM4','3P0EM4','5P0EM4','8P0EM4','1P0EM3','3P0EM3','5P0EM3','8P0EM3','1P0EM2','3P0EM2','5P0EM2','8P0EM2','1P0EM1'])

	for i in xrange(len(time)):
		idx = np.argmin(np.abs(time[i]-ftimes)) #compare chk file times to the times of 'equilibrium'
		rfiles.append(files[idx])

		idx2 = np.argmin(np.abs(fvalues-IP_V[i]))
		IP.append(fvalues[idx2])
		IPN.append(fnames[idx2])
    		#ipstr = fnames[idx]
    '''
    for i in xrange(len(times)):
        print 'ID: %i J21: %6.4e IP: %6.4e time: %6.4e file: %s'%(ids[i],cj21s[i],IP_Vs[i],times[i],files[i])
    return IP_Vs,files,np.array(ids),np.array(cj21s)



def read_par(ldata):
    nspec = 64
    nion  = 12
    data = np.zeros(nspec)
    dion = np.zeros(nion)

    data[:] = ldata[23:87] #select out the fractions from H to electrons
    dion[0]  = np.sum(data[0:2])   #H
    dion[1]  = np.sum(data[2:5])   #He
    dion[2]  = np.sum(data[5:11])  #C
    dion[3]  = np.sum(data[11:18]) #N
    dion[4]  = np.sum(data[18:26]) #O
    dion[5]  = np.sum(data[26:36]) #Ne
    dion[6]  = np.sum(data[36:39]) #Na
    dion[7]  = np.sum(data[39:43]) #Mg
    dion[8]  = np.sum(data[43:49]) #Si
    dion[9]  = np.sum(data[49:54]) #S
    dion[10] = np.sum(data[54:59]) #Ca
    dion[11] = np.sum(data[59:64]) #Fe
    #dion[12] = data[65] #don't do electrons
    #print dion
    return data,dion

def calc_xpdf(xpdf,data,specid):
    pdf  = xpdf['ones']
    den  = xpdf.x.v #['density']
    temp = xpdf.y.v #['temperature']

    dens= np.sum(den*pdf)
    xS   = np.interp(temp,data[:,0],data[:,specid])
    xS   = np.where(xS < 1.0e-30, 1.0e-30, xS)
    xS   = np.sum(xS*den*pdf)/dens
    return xS

def calc_xtpdf(xpdf,data,specid):
    pdf  = xpdf['ones']
    den  = xpdf.x.v #['density']
    temp = xpdf.y.v #['temperature']

    x   = np.interp(temp,data[:,0],data[:,specid])
    x   = np.where(x < 1.0e-30, 1.0e-30, x)
    bot = np.sum(x*den*pdf)
    top = np.sum(x*den*temp*pdf)
    xS  = top/bot
    return xS

def make_slices(fn,pf,dd,fout):
    fin = fn
    M = pf.domain_dimensions[0]

    dens = dd['density']
    temp = dd['temperature']
    vol = dd['dx']*dd['dy']*dd['dz']
    tmass = dd.quantities['TotalMass']()
    cdens = np.where( dd['temperature'] < 1.0e4 , dens*vol, 0.0)
    cdens =  cdens.sum()/1.989e33

    dwtemp = np.sum( dd['density']*dd['temperature'] ) / np.sum(dd['density'])
    vwtemp = np.sum( vol * dd['temperature'] ) / np.sum(vol)

    abar = np.average(dd['myabar'])
    v_vel = np.sum( vol * (dd['velx']*dd['velx']+dd['vely']*dd['vely']+dd['velz']*dd['velz']) ) / np.sum(vol)
    v_vel = np.sqrt(v_vel)

    d_vel = np.sum( (dd['density']) * (dd['velx']*dd['velx']+dd['vely']*dd['vely']+dd['velz']*dd['velz']) ) / np.sum(dd['density'])
    d_vel = np.sqrt(d_vel)

    cs = 5./3. * kboltz * dwtemp / (abar * mh)
    cs = np.sqrt(cs)

    vwmn = v_vel/cs
    dwmn = d_vel/cs

    print 'V_VEL: ', v_vel
    print 'D_VEL: ', d_vel
    print 'ABAR:  ', abar
    print 'CS:    ', cs
    print 'VWMN:  ', vwmn
    print 'DWMN:  ', dwmn

    ln = 'DENSITY-WEIGHTED-TEMP: %.3f \n'%(dwtemp)
    fout.write(ln)
    ln = 'VOLUME-WEIGHTED-TEMP: %.3f \n'%(vwtemp)
    fout.write(ln)
    ln = 'DENSITY-WEIGHTED-M: %.3f \n'%(dwmn)
    fout.write(ln)
    ln = 'VOLUME-WEIGHTED-M: %.3f \n'%(vwmn)
    fout.write(ln)

    p = SlicePlot(pf,2,'temperature',center='c')
    p.set_cmap('temperature','Rainbow')
    p.annotate_contour('temperature',ncont=32,factor=4,take_log=True)
    ln = 'temp_%s.pdf'%(fn[-4:])
    p.save(ln)

    p = SlicePlot(pf,2,'ndens',center='c')
    p.set_cmap('ndens','Rainbow')
    p.annotate_contour('ndens',ncont=32,factor=4,take_log=True)
    ln = 'ndens_%s.pdf'%(str(fn[-4:]))
    p.save(ln)

def make_2dpdf(fn,pf,dd):
    fin = fn
    M = pf.domain_dimensions[0]
    tmax = np.max(dd['temperature'])*10.
    tmin = np.min(dd['temperature'])*0.1
    dmax = np.max(dd['ndens'])*10.
    dmin = np.min(dd['ndens'])*0.1

    #prof2d = BinnedProfile2D(dd,128,'ndens',dmin,dmax,True,128,'temperature',tmin,tmax,True)
    prof2d = create_profile(data_source=dd,bin_fields=["ndens","temperature"],fields=["ones"],n_bins=128,extrema=dict(ndens=(dmin,dmax),temperature=(tmin,tmax)),logs=dict(ndens=True,temperature=True))
    x = np.log10(prof2d.x.v)
    y = np.log10(prof2d.y.v)
    #x = np.log10(prof2d['temperature'])
    #y = np.log10(prof2d['ndens'])
    #prof2d.add_fields("ones",weight=None,fractional=True)

    X,Y = np.meshgrid(x,y)
    data = (prof2d['ones'])
    data = data/np.sum(data)
    data = np.log10(data)
    data = np.where( prof2d.used == True , data, -10.0)
    data = np.max(data) - data

    levinverse = (np.linspace(0,121,num=121,endpoint=True)/100.-0.2)*np.max(data)
    lev = np.array([0.01,0.03,0.1,0.3,0.99])
    lev = lev * np.max(data)

    fig = plt.figure()
    plt.subplot(111)
    ax=plt.gca()

    my_cmap = matplotlib.cm.get_cmap('Eos B')
    my_cmap.set_over('w')
    myvmax = np.max(data) - 0.1
    ax.contourf(Y,X,data,levinverse,cmap=my_cmap,vmax=myvmax)

    cs=ax.contour(Y,X,data,lev,colors='k')
    strs = ['1.0' ,'0.3' ,'0.1','0.03', '0.01']
    fmt={}
    for l,s in zip(cs.levels, strs):
        fmt[l] = s
    ax.clabel(cs,colors='k',inline=1,fmt=fmt,fontsize=8)

    val = np.log10(60./48.5)*2.+5.+.2
    ax.axhline(y=val,color='k')

    plt.xlabel('lg density')
    plt.ylabel('lg T')
    plt.xlim([np.log10(dmin),np.log10(dmax)])
    plt.ylim([np.log10(tmin),np.log10(tmax)])
    ln = 'pdf2d_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)
    ln = 'pdf2d_data_%s_x.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d.x.v)
    ln = 'pdf2d_data_%s_y.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d.y.v)
    ln = 'pdf2d_data_%s_v.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d['ones'].v)
    plt.close(fig)

def make_2ddpdf(fn,pf,dd):
    fin = fn
    M = pf.domain_dimensions[0]
    tmax = np.max(dd['temperature'])*10.
    tmin = np.min(dd['temperature'])*0.1
    dmax = np.max(dd['ndens'])*10.
    dmin = np.min(dd['ndens'])*0.1

    prof2d = create_profile(data_source=dd,bin_fields=["ndens","temperature"],fields=["density"],n_bins=128,extrema=dict(ndens=(dmin,dmax),temperature=(tmin,tmax)),logs=dict(ndens=True,temperature=True))
    x = np.log10(prof2d.x.v)
    y = np.log10(prof2d.y.v)
    #prof2d = BinnedProfile2D(dd,128,'ndens',dmin,dmax,True,128,'temperature',tmin,tmax,True)
    #x = np.log10(prof2d['temperature'])
    #y = np.log10(prof2d['ndens'])
    #prof2d.add_fields("density",weight=None,fractional=True)

    X,Y = np.meshgrid(x,y)
    data = (prof2d['density'])
    data = data/np.sum(data)
    data = np.log10(data)
    data = np.where( prof2d.used == True , data, -10.0)
    data = np.max(data) - data

    levinverse = (np.linspace(0,121,num=121,endpoint=True)/100.-0.2)*np.max(data)
    lev = np.array([0.01,0.03,0.1,0.3,0.99])
    lev = lev * np.max(data)

    fig = plt.figure()
    plt.subplot(111)
    ax=plt.gca()

    my_cmap = matplotlib.cm.get_cmap('Eos B')
    my_cmap.set_over('w')
    myvmax = np.max(data) - 0.1
    ax.contourf(Y,X,data,levinverse,cmap=my_cmap,vmax=myvmax)

    cs=ax.contour(Y,X,data,lev,colors='k')
    strs = ['1.0' ,'0.3' ,'0.1','0.03', '0.01']
    fmt={}
    for l,s in zip(cs.levels, strs):
        fmt[l] = s
    ax.clabel(cs,colors='k',inline=1,fmt=fmt,fontsize=8)

    val = np.log10(60./48.5)*2.+5.+.2
    ax.axhline(y=val,color='k')

    plt.xlabel('lg density')
    plt.ylabel('lg T')
    plt.xlim([np.log10(dmin),np.log10(dmax)])
    plt.ylim([np.log10(tmin),np.log10(tmax)])
    ln = 'pdf2dd_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)

    ln = 'pdf2dd_data_%s_x.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d.x.v)
    ln = 'pdf2dd_data_%s_y.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d.y.v)
    ln = 'pdf2dd_data_%s_v.txt'%(str(fn[-4:]))
    np.savetxt(ln,prof2d['density'].v)
    plt.close(fig)

def make_1dpdf(fn,pf,dd):
    fin = fn
    M = pf.domain_dimensions[0]
    tmin = np.min(dd['temperature'])*0.1
    tmax = np.max(dd['temperature'])*10.

    #temppdf = BinnedProfile1D(dd,128,'temperature',tmin,tmax,True)
    #temppdf.add_fields("ones",weight=None,fractional=True)
    temppdf = create_profile(data_source=dd,bin_fields=["temperature"],fields=["ones"],n_bins=128,extrema=dict(temperature=(tmin,tmax)),logs=dict(temperature=True))
    fig = plt.figure()
    plt.subplot(111)
    ax=plt.gca()

    ax.loglog(temppdf.x.v,temppdf["ones"],lw=3,label='TempPDF')
    #ax.loglog(temppdf["temperature"],temppdf["ones"],lw=3,label='TempPDF')
    ax.set_xlabel(r'Temperature [K]')
    ax.set_ylabel(r'PDF')
    ln = '1dpdf_temp_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)
    plt.close(fig)

    dmax = np.max(dd['ndens'])*10.
    dmin = np.min(dd['ndens'])*0.1
    #denpdf = BinnedProfile1D(dd,128,'ndens',dmin,dmax,True)
    #denpdf.add_fields("ones",weight=None,fractional=True)
    denpdf = create_profile(data_source=dd,bin_fields=["ndens"],fields=["ones"],n_bins=128,extrema=dict(ndens=(dmin,dmax)),logs=dict(temperature=True))
    fig = plt.figure()
    plt.subplot(111)
    ax=plt.gca()

    ax.loglog(denpdf.x.v,denpdf["ones"],lw=3,label='ndensPDF')
    ax.set_xlabel(r'n [cm$^{-3}$]')
    ax.set_ylabel(r'PDF')
    ln = '1dpdf_ndens_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)
    plt.close(fig)

    ln = '1dpdf_temppdf_%s.txt'%(str(fn[-4:]))
    savedata = np.zeros((2,128))
    savedata[0,:] = temppdf.x.v
    savedata[1,:] = temppdf["ones"]
    np.savetxt(ln,savedata)
    #temppdf.write_out(ln)
    ln = '1dpdf_denpdf_%s.txt'%(str(fn[-4:]))
    savedata = np.zeros((2,128))
    savedata[0,:] = temppdf.x.v
    savedata[1,:] = temppdf["ones"]
    np.savetxt(ln,savedata)
    #denpdf.write_out(ln)

def get_stats(fn,pf,dd,fout):
    fin = fn
    M = 128

    dmax = np.max(dd['xvar'])*2.
    dmin = np.min(dd['xvar'])*2.
    #xpdf = BinnedProfile1D(dd,128,'xvar',dmax,dmin,False)
    #xpdf.add_fields("ones",weight=None,fractional=True)
    xpdf = create_profile(data_source=dd,bin_fields=["xvar"],fields=["ones"],n_bins=128,extrema=dict(xvar=(dmin,dmax)),logs=dict(xvar=False),fractional=True)
    ln = '1dpdf_xvarpdf_%s.txt'%(str(fn[-4:]))
    savedata = np.zeros((2,128))
    savedata[0,:] = xpdf.x.v
    savedata[1,:] = xpdf["ones"]
    np.savetxt(ln,savedata)
    #xpdf.write_out(ln)

    fig = plt.figure()
    plt.subplot(111)
    ax=plt.gca()

    ax.semilogy(xpdf.x.v,xpdf["ones"],lw=3,label='xPDF')
    ax.set_xlim([-5,5])
    ax.set_xlabel(r'ln$\left(\frac{\rho}{\bar{\rho}} \right)$')
    ax.set_ylabel(r'PDF')
    ln = '1dpdf_xvarpdf_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)
    plt.close(fig)

    x  = xpdf.x.v  #xpdf['xvar']
    Nx = xpdf['ones']

    temp1 = np.sum(x*Nx)
    mymean = temp1
    temp2 = np.sum((x-mymean)**2*Nx)
    temp3 = np.sum((x-mymean)**3*Nx)
    temp4 = np.sum((x-mymean)**4*Nx)

    myvar  = temp2
    myskew = temp3/temp2**1.5
    mykurt = temp4/temp2**2 - 3.0 #- 3.0 With this, it is the kurtosis excess

    ln = 'mean: %6.4e\n'%(mymean)
    fout.write(ln)
    ln = 'var: %6.4e\n'%(np.sqrt(myvar))
    fout.write(ln)
    ln = 'skew: %6.4e\n'%(myskew)
    fout.write(ln)
    ln = 'kurt: %6.4e\n'%(mykurt)
    fout.write(ln)


def get_chem(dire,fn,pf,dd,fout,lineid,j21_value):
    ln = dire+'KH.dat'
    adata = np.loadtxt(ln,skiprows=1)
    den = 1.0 #first row of data from .dat
    data = adata[int(lineid),:]  #one row of .dat at the time of interest
    nhtot = (data[23]+data[24])*den/mh
    IP = j21_value * 4.1735e-05 / nhtot
    #idata,ipname = get_ion(IP)

    ln = 'CHEM_J21: %6.4e\n'%(j21_value)
    fout.write(ln)
    ln = 'CHEM_IP: %6.4e\n'%(IP)
    fout.write(ln)

#data[i] is from .dat - i corresponds to the column for the ion   (but this is the column number -1 if you're looking at the .dat header numbers)

    meant = data[8]
    smf,imf = read_par(data)

    #maxden = np.max(dd['density'])*10.
    #minden = np.min(dd['density'])*0.1
    #prof2d = BinnedProfile2D(dd,128,'density',minden,maxden,True,128,'temperature',1e2,1e8,True)
    #prof2d.add_fields("ones",weight=None,fractional=True)
    #fout.write('\n\n')

    tmax = np.max(dd['temp'])*10.
    tmin = np.min(dd['temp'])*0.1
    dmax = np.max(dd['density'])*10.
    dmin = np.min(dd['density'])*0.1
    prof2d = create_profile(data_source=dd,bin_fields=["density","temperature"],fields=["ones"],n_bins=128,extrema=dict(density=(dmin,dmax),temperature=(tmin,tmax)),logs=dict(density=True,temperature=True))
    fout.write('\n\n')

    ##Print    - Ion Name, Mass Fraction, Density Weighted Temperature, Density weighted (curr_ke = 0.5 * velx **2 + vely**2 + velz**2 ))
    ln = ''
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-10s\t%-10s\t%-10s\t%-10s\n'      %('Spec','MFrac','DW_Temp','DW_VD','Doppler') )
    #fout.write( '\n%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s\n'      %('Spec','MFrac','DW_Temp','DW_VD','Doppler','CIEX','<X(T)>','<T-X(T)>') )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('H'   ,data[23]/imf[0], data[153], np.sqrt(2.0*data[88])/1.0e5, np.sqrt((2.0*data[88]/3.0) + (2.0*kboltz*data[153])/(1.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,1]) , calc_xpdf(prof2d,idata,1) , calc_xtpdf(prof2d,idata,1)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('H+'  ,data[24]/imf[0], data[154], np.sqrt(2.0*data[89])/1.0e5, np.sqrt((2.0*data[89]/3.0) + (2.0*kboltz*data[154])/(1.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,2]) , calc_xpdf(prof2d,idata,2) , calc_xtpdf(prof2d,idata,2)  ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('He'  ,data[25]/imf[1], data[155], np.sqrt(2.0*data[90])/1.0e5, np.sqrt((2.0*data[90]/3.0) + (2.0*kboltz*data[155])/(4.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,3]) , calc_xpdf(prof2d,idata,3) , calc_xtpdf(prof2d,idata,3)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('He+' ,data[26]/imf[1], data[156], np.sqrt(2.0*data[91])/1.0e5, np.sqrt((2.0*data[91]/3.0) + (2.0*kboltz*data[156])/(4.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,4]) , calc_xpdf(prof2d,idata,4) , calc_xtpdf(prof2d,idata,4)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('He2+',data[27]/imf[1], data[157], np.sqrt(2.0*data[92])/1.0e5, np.sqrt((2.0*data[92]/3.0) + (2.0*kboltz*data[157])/(4.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,5]) , calc_xpdf(prof2d,idata,5) , calc_xtpdf(prof2d,idata,5)  ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C'   ,data[28]/imf[2], data[158], np.sqrt(2.0*data[93])/1.0e5, np.sqrt((2.0*data[93]/3.0) + (2.0*kboltz*data[158])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,6]) , calc_xpdf(prof2d,idata,6) , calc_xtpdf(prof2d,idata,6)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C+'  ,data[29]/imf[2], data[159], np.sqrt(2.0*data[94])/1.0e5, np.sqrt((2.0*data[94]/3.0) + (2.0*kboltz*data[159])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,7]) , calc_xpdf(prof2d,idata,7) , calc_xtpdf(prof2d,idata,7)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C2+' ,data[30]/imf[2], data[160], np.sqrt(2.0*data[95])/1.0e5, np.sqrt((2.0*data[95]/3.0) + (2.0*kboltz*data[160])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,8]) , calc_xpdf(prof2d,idata,8) , calc_xtpdf(prof2d,idata,8)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C3+' ,data[31]/imf[2], data[161], np.sqrt(2.0*data[96])/1.0e5, np.sqrt((2.0*data[96]/3.0) + (2.0*kboltz*data[161])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,9]) , calc_xpdf(prof2d,idata,9) , calc_xtpdf(prof2d,idata,9)  ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C4+' ,data[32]/imf[2], data[162], np.sqrt(2.0*data[97])/1.0e5, np.sqrt((2.0*data[97]/3.0) + (2.0*kboltz*data[162])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,10]), calc_xpdf(prof2d,idata,10), calc_xtpdf(prof2d,idata,10) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('C5+' ,data[33]/imf[2], data[163], np.sqrt(2.0*data[98])/1.0e5, np.sqrt((2.0*data[98]/3.0) + (2.0*kboltz*data[163])/(12.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,11]), calc_xpdf(prof2d,idata,11), calc_xtpdf(prof2d,idata,11) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N'   ,data[34]/imf[3], data[164], np.sqrt(2.0*data[99])/1.0e5, np.sqrt((2.0*data[99]/3.0) + (2.0*kboltz*data[164])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,12]), calc_xpdf(prof2d,idata,12), calc_xtpdf(prof2d,idata,12) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N+'  ,data[35]/imf[3], data[165], np.sqrt(2.0*data[100])/1.0e5, np.sqrt((2.0*data[100]/3.0) + (2.0*kboltz*data[165])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,13]), calc_xpdf(prof2d,idata,13), calc_xtpdf(prof2d,idata,13) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N2+' ,data[36]/imf[3], data[166], np.sqrt(2.0*data[101])/1.0e5, np.sqrt((2.0*data[101]/3.0) + (2.0*kboltz*data[166])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,14]), calc_xpdf(prof2d,idata,14), calc_xtpdf(prof2d,idata,14) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N3+' ,data[37]/imf[3], data[167], np.sqrt(2.0*data[102])/1.0e5, np.sqrt((2.0*data[102]/3.0) + (2.0*kboltz*data[167])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,15]), calc_xpdf(prof2d,idata,15), calc_xtpdf(prof2d,idata,15) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N4+' ,data[38]/imf[3], data[168], np.sqrt(2.0*data[103])/1.0e5, np.sqrt((2.0*data[103]/3.0) + (2.0*kboltz*data[168])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,16]), calc_xpdf(prof2d,idata,16), calc_xtpdf(prof2d,idata,16) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N5+' ,data[39]/imf[3], data[169], np.sqrt(2.0*data[104])/1.0e5, np.sqrt((2.0*data[104]/3.0) + (2.0*kboltz*data[169])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,17]), calc_xpdf(prof2d,idata,17), calc_xtpdf(prof2d,idata,17) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('N6+' ,data[40]/imf[3], data[170], np.sqrt(2.0*data[105])/1.0e5, np.sqrt((2.0*data[105]/3.0) + (2.0*kboltz*data[170])/(14.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,18]), calc_xpdf(prof2d,idata,18), calc_xtpdf(prof2d,idata,18) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O'   ,data[41]/imf[4], data[171], np.sqrt(2.0*data[106])/1.0e5, np.sqrt((2.0*data[106]/3.0) + (2.0*kboltz*data[171])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,19]), calc_xpdf(prof2d,idata,19), calc_xtpdf(prof2d,idata,19) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O+'  ,data[42]/imf[4], data[172], np.sqrt(2.0*data[107])/1.0e5, np.sqrt((2.0*data[107]/3.0) + (2.0*kboltz*data[172])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,20]), calc_xpdf(prof2d,idata,20), calc_xtpdf(prof2d,idata,20) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O2+' ,data[43]/imf[4], data[173], np.sqrt(2.0*data[108])/1.0e5, np.sqrt((2.0*data[108]/3.0) + (2.0*kboltz*data[173])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,21]), calc_xpdf(prof2d,idata,21), calc_xtpdf(prof2d,idata,21) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O3+' ,data[44]/imf[4], data[174], np.sqrt(2.0*data[109])/1.0e5, np.sqrt((2.0*data[109]/3.0) + (2.0*kboltz*data[174])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,22]), calc_xpdf(prof2d,idata,22), calc_xtpdf(prof2d,idata,22) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O4+' ,data[45]/imf[4], data[175], np.sqrt(2.0*data[110])/1.0e5, np.sqrt((2.0*data[110]/3.0) + (2.0*kboltz*data[175])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,23]), calc_xpdf(prof2d,idata,23), calc_xtpdf(prof2d,idata,23) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O5+' ,data[46]/imf[4], data[176], np.sqrt(2.0*data[111])/1.0e5, np.sqrt((2.0*data[111]/3.0) + (2.0*kboltz*data[176])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,24]), calc_xpdf(prof2d,idata,24), calc_xtpdf(prof2d,idata,24) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O6+' ,data[47]/imf[4], data[177], np.sqrt(2.0*data[112])/1.0e5, np.sqrt((2.0*data[112]/3.0) + (2.0*kboltz*data[177])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,25]), calc_xpdf(prof2d,idata,25), calc_xtpdf(prof2d,idata,25) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('O7+' ,data[48]/imf[4], data[178], np.sqrt(2.0*data[113])/1.0e5, np.sqrt((2.0*data[113]/3.0) + (2.0*kboltz*data[178])/(16.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,26]), calc_xpdf(prof2d,idata,26), calc_xtpdf(prof2d,idata,26) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne'  ,data[49]/imf[5], data[179], np.sqrt(2.0*data[114])/1.0e5 , np.sqrt((2.0*data[114]/3.0)  + (2.0*kboltz*data[179])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,27]), calc_xpdf(prof2d,idata,27), calc_xtpdf(prof2d,idata,27) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne+' ,data[50]/imf[5], data[180], np.sqrt(2.0*data[115])/1.0e5 , np.sqrt((2.0*data[115]/3.0)  + (2.0*kboltz*data[180])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,28]), calc_xpdf(prof2d,idata,28), calc_xtpdf(prof2d,idata,28) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne2+',data[51]/imf[5], data[181], np.sqrt(2.0*data[116])/1.0e5 , np.sqrt((2.0*data[116]/3.0)  + (2.0*kboltz*data[181])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,29]), calc_xpdf(prof2d,idata,29), calc_xtpdf(prof2d,idata,29) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne3+',data[52]/imf[5], data[182], np.sqrt(2.0*data[117])/1.0e5 , np.sqrt((2.0*data[117]/3.0)  + (2.0*kboltz*data[182])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,30]), calc_xpdf(prof2d,idata,30), calc_xtpdf(prof2d,idata,30) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne4+',data[53]/imf[5], data[183], np.sqrt(2.0*data[118])/1.0e5 , np.sqrt((2.0*data[118]/3.0)  + (2.0*kboltz*data[183])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,31]), calc_xpdf(prof2d,idata,31), calc_xtpdf(prof2d,idata,31) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne5+',data[54]/imf[5], data[184], np.sqrt(2.0*data[119])/1.0e5 , np.sqrt((2.0*data[119]/3.0)  + (2.0*kboltz*data[184])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,32]), calc_xpdf(prof2d,idata,32), calc_xtpdf(prof2d,idata,32) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne6+',data[55]/imf[5], data[185], np.sqrt(2.0*data[120])/1.0e5 , np.sqrt((2.0*data[120]/3.0)  + (2.0*kboltz*data[185])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,33]), calc_xpdf(prof2d,idata,33), calc_xtpdf(prof2d,idata,33) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne7+',data[56]/imf[5], data[186], np.sqrt(2.0*data[121])/1.0e5, np.sqrt((2.0*data[121]/3.0) + (2.0*kboltz*data[186])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,34]), calc_xpdf(prof2d,idata,34), calc_xtpdf(prof2d,idata,34) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne8+',data[57]/imf[5], data[187], np.sqrt(2.0*data[122])/1.0e5, np.sqrt((2.0*data[122]/3.0) + (2.0*kboltz*data[187])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,35]), calc_xpdf(prof2d,idata,35), calc_xtpdf(prof2d,idata,35) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ne9+',data[58]/imf[5], data[188], np.sqrt(2.0*data[123])/1.0e5, np.sqrt((2.0*data[123]/3.0) + (2.0*kboltz*data[188])/(20.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,36]), calc_xpdf(prof2d,idata,36), calc_xtpdf(prof2d,idata,36) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Na'  ,data[59]/imf[6], data[189], np.sqrt(2.0*data[124])/1.0e5, np.sqrt((2.0*data[124]/3.0) + (2.0*kboltz*data[189])/(23.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,37]), calc_xpdf(prof2d,idata,37), calc_xtpdf(prof2d,idata,37) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Na+' ,data[60]/imf[6], data[190], np.sqrt(2.0*data[125])/1.0e5, np.sqrt((2.0*data[125]/3.0) + (2.0*kboltz*data[190])/(23.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,38]), calc_xpdf(prof2d,idata,38), calc_xtpdf(prof2d,idata,38) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Na2+',data[61]/imf[6], data[191], np.sqrt(2.0*data[126])/1.0e5, np.sqrt((2.0*data[126]/3.0) + (2.0*kboltz*data[191])/(23.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,39]), calc_xpdf(prof2d,idata,39), calc_xtpdf(prof2d,idata,39) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Mg'  ,data[62]/imf[7], data[192], np.sqrt(2.0*data[127])/1.0e5, np.sqrt((2.0*data[127]/3.0) + (2.0*kboltz*data[192])/(24.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,40]), calc_xpdf(prof2d,idata,40), calc_xtpdf(prof2d,idata,40) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Mg+' ,data[63]/imf[7], data[193], np.sqrt(2.0*data[128])/1.0e5, np.sqrt((2.0*data[128]/3.0) + (2.0*kboltz*data[193])/(24.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,41]), calc_xpdf(prof2d,idata,41), calc_xtpdf(prof2d,idata,41) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Mg2+',data[64]/imf[7], data[194], np.sqrt(2.0*data[129])/1.0e5, np.sqrt((2.0*data[129]/3.0) + (2.0*kboltz*data[194])/(24.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,42]), calc_xpdf(prof2d,idata,42), calc_xtpdf(prof2d,idata,42) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Mg3+',data[65]/imf[7], data[195], np.sqrt(2.0*data[130])/1.0e5, np.sqrt((2.0*data[130]/3.0) + (2.0*kboltz*data[195])/(24.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,43]), calc_xpdf(prof2d,idata,43), calc_xtpdf(prof2d,idata,43) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si'  ,data[66]/imf[8], data[196], np.sqrt(2.0*data[131])/1.0e5, np.sqrt((2.0*data[131]/3.0) + (2.0*kboltz*data[196])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,44]), calc_xpdf(prof2d,idata,44), calc_xtpdf(prof2d,idata,44) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si+' ,data[67]/imf[8], data[197], np.sqrt(2.0*data[132])/1.0e5, np.sqrt((2.0*data[132]/3.0) + (2.0*kboltz*data[197])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,45]), calc_xpdf(prof2d,idata,45), calc_xtpdf(prof2d,idata,45) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si2+',data[68]/imf[8], data[198], np.sqrt(2.0*data[133])/1.0e5, np.sqrt((2.0*data[133]/3.0) + (2.0*kboltz*data[198])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,46]), calc_xpdf(prof2d,idata,46), calc_xtpdf(prof2d,idata,46) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si3+',data[69]/imf[8], data[199], np.sqrt(2.0*data[134])/1.0e5, np.sqrt((2.0*data[134]/3.0) + (2.0*kboltz*data[199])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,47]), calc_xpdf(prof2d,idata,47), calc_xtpdf(prof2d,idata,47) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si4+',data[70]/imf[8], data[200], np.sqrt(2.0*data[135])/1.0e5, np.sqrt((2.0*data[135]/3.0) + (2.0*kboltz*data[200])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,48]), calc_xpdf(prof2d,idata,48), calc_xtpdf(prof2d,idata,48) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Si5+',data[71]/imf[8], data[201], np.sqrt(2.0*data[136])/1.0e5, np.sqrt((2.0*data[136]/3.0) + (2.0*kboltz*data[201])/(28.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,49]), calc_xpdf(prof2d,idata,49), calc_xtpdf(prof2d,idata,49) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('S'   ,data[72]/imf[9], data[202], np.sqrt(2.0*data[137])/1.0e5, np.sqrt((2.0*data[137]/3.0) + (2.0*kboltz*data[202])/(32.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,50]), calc_xpdf(prof2d,idata,50), calc_xtpdf(prof2d,idata,50) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('S+'  ,data[73]/imf[9], data[203], np.sqrt(2.0*data[138])/1.0e5, np.sqrt((2.0*data[138]/3.0) + (2.0*kboltz*data[203])/(32.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,51]), calc_xpdf(prof2d,idata,51), calc_xtpdf(prof2d,idata,51) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('S2+' ,data[74]/imf[9], data[204], np.sqrt(2.0*data[139])/1.0e5, np.sqrt((2.0*data[139]/3.0) + (2.0*kboltz*data[204])/(32.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,52]), calc_xpdf(prof2d,idata,52), calc_xtpdf(prof2d,idata,52) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('S3+' ,data[75]/imf[9], data[205], np.sqrt(2.0*data[140])/1.0e5, np.sqrt((2.0*data[140]/3.0) + (2.0*kboltz*data[205])/(32.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,53]), calc_xpdf(prof2d,idata,53), calc_xtpdf(prof2d,idata,53) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('S4+' ,data[76]/imf[9], data[206], np.sqrt(2.0*data[141])/1.0e5, np.sqrt((2.0*data[141]/3.0) + (2.0*kboltz*data[206])/(32.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,54]), calc_xpdf(prof2d,idata,54), calc_xtpdf(prof2d,idata,54) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ca'  ,data[77]/imf[10], data[207], np.sqrt(2.0*data[142])/1.0e5, np.sqrt((2.0*data[142]/3.0) + (2.0*kboltz*data[207])/(40.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,55]), calc_xpdf(prof2d,idata,55), calc_xtpdf(prof2d,idata,55) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ca+' ,data[78]/imf[10], data[208], np.sqrt(2.0*data[143])/1.0e5, np.sqrt((2.0*data[143]/3.0) + (2.0*kboltz*data[208])/(40.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,56]), calc_xpdf(prof2d,idata,56), calc_xtpdf(prof2d,idata,56) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ca2+',data[79]/imf[10], data[209], np.sqrt(2.0*data[144])/1.0e5, np.sqrt((2.0*data[144]/3.0) + (2.0*kboltz*data[209])/(40.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,57]), calc_xpdf(prof2d,idata,57), calc_xtpdf(prof2d,idata,57) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ca3+',data[80]/imf[10], data[210], np.sqrt(2.0*data[145])/1.0e5, np.sqrt((2.0*data[145]/3.0) + (2.0*kboltz*data[210])/(40.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,58]), calc_xpdf(prof2d,idata,58), calc_xtpdf(prof2d,idata,58) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Ca4+',data[81]/imf[10], data[211], np.sqrt(2.0*data[146])/1.0e5, np.sqrt((2.0*data[146]/3.0) + (2.0*kboltz*data[211])/(40.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,59]), calc_xpdf(prof2d,idata,59), calc_xtpdf(prof2d,idata,59) ) )
    fout.write( ln.ljust(122,'-') )
    fout.write( '\n%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Fe'  ,data[82]/imf[11], data[212], np.sqrt(2.0*data[147])/1.0e5, np.sqrt((2.0*data[147]/3.0) + (2.0*kboltz*data[212])/(56.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,60]), calc_xpdf(prof2d,idata,60), calc_xtpdf(prof2d,idata,60) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Fe+' ,data[83]/imf[11], data[213], np.sqrt(2.0*data[148])/1.0e5, np.sqrt((2.0*data[148]/3.0) + (2.0*kboltz*data[213])/(56.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,61]), calc_xpdf(prof2d,idata,61), calc_xtpdf(prof2d,idata,61) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Fe2+',data[84]/imf[11], data[214], np.sqrt(2.0*data[149])/1.0e5, np.sqrt((2.0*data[149]/3.0) + (2.0*kboltz*data[214])/(56.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,62]), calc_xpdf(prof2d,idata,62), calc_xtpdf(prof2d,idata,62) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Fe3+',data[85]/imf[11], data[215], np.sqrt(2.0*data[150])/1.0e5, np.sqrt((2.0*data[150]/3.0) + (2.0*kboltz*data[215])/(56.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,63]), calc_xpdf(prof2d,idata,63), calc_xtpdf(prof2d,idata,63) ) )
    fout.write(   '%-10s\t%-6.4e\t%-6.4e\t%-6.4e\t%-6.4e\n'%('Fe4+',data[86]/imf[11], data[216], np.sqrt(2.0*data[151])/1.0e5, np.sqrt((2.0*data[151]/3.0) + (2.0*kboltz*data[216])/(56.0*mh))/1.0e5))#, np.interp(meant,idata[:,0],idata[:,64]), calc_xpdf(prof2d,idata,64), calc_xtpdf(prof2d,idata,64) ) )
    fout.write( ln.ljust(122,'-') )

def get_power(fn,pf,dd,fout):
    fin = fn
    M = int(pf.domain_dimensions[0])
    n = np.array([int(M),int(M),int(M)])
    k0 = 0
    kc = M/2

    reg = pf.h.covering_grid(0,left_edge=pf.domain_left_edge,dims=[M,M,M])
    vx = reg['velx']
    vy = reg['vely']
    vz = reg['velz']
    s = np.array([M,M,M])
    axes = np.array([0,1,2])
    vx = np.abs( np.fft.fftn(vx,s,axes) ) / float(M**3)
    vy = np.abs( np.fft.fftn(vy,s,axes) ) / float(M**3)
    vz = np.abs( np.fft.fftn(vz,s,axes) ) / float(M**3)

    kx = np.zeros(n)
    ky = np.zeros(n)
    kz = np.zeros(n)

    for j in range(0,n[1]):
        for k in range (0,n[2]):
            kx[:,j,k] = n[0]*np.fft.fftfreq(n[0])
    for i in range(0,n[0]):
        for k in range (0,n[2]):
            ky[i,:,k] = n[1]*np.fft.fftfreq(n[1])
    for i in range(0,n[0]):
        for j in range (0,n[1]):
            kz[i,j,:] = n[2]*np.fft.fftfreq(n[2])

    k = np.sqrt( (kx**2+ky**2+kz**2) )

    k1d=[]
    power=[]
    for i in range(k0,kc+1):
        si = np.where( np.logical_and( k>=float(i),k<float(i+1) ) )
        k1d.append(i)
        power.append( np.sum( vx[si]**2 + vy[si]**2 + vz[si]**2 ) )
    k1d=np.array(k1d)
    power=np.array(power)

    fig = plt.figure()
    plt.clf()
    plt.loglog(k1d,power,'b',lw=3)
    plt.xlabel(r'k/2$\pi$')
    plt.ylabel('E(k)')
    plt.xlim([1,M])
    ln = 'power_%s.pdf'%(str(fn[-4:]))
    plt.savefig(ln)
    plt.close(fig)

def move_stuff():
	curr_dir = subprocess.check_output('pwd',shell=True)
	ln = str.split(curr_dir)[0]+'/Figs'
	check = os.path.isdir(ln)
	if(check == True):
		ln = 'rm -rf Figs'
		subprocess.check_output(ln,shell=True)
		ln = 'mkdir Figs'
		subprocess.check_output(ln,shell=True)
	else:
		ln = 'mkdir Figs'
		subprocess.check_output(ln,shell=True)
	#move pdfs
	ln = 'mv *.pdf Figs/'
	subprocess.check_output(ln,shell=True)
	ln = 'mv ISM_info*.dat 1d*.txt 2d*.txt pdf2d*.txt Figs'
	subprocess.check_output(ln,shell=True)

def main():
    if( len(sys.argv[1:]) != 1):
        sys.exit('USAGE: python pdf.py DIRECTORY')
    else:
    	dire = str(sys.argv[1])

    IP,uvfiles,cs,j21=get_uvfiles(dire)
    #files = glob.glob(dire+'KH_hdf5_chk_*')
    #cs = np.arange(len(files))
    #j21 = np.ones(len(files))
    #nfiles = len(files)

    for i in range(len(uvfiles)):
        print 'WORKING ON: ', uvfiles[i]
        pf = load(uvfiles[i])
        dd = pf.h.all_data()
        fid = uvfiles[i][-4:]
        ln = dire+'KH_info_'+str(fid)+'.dat'
        fout = open(ln,'w')
        fn = uvfiles[i]

        #make_slices(fn,pf,dd,fout)
        #make_2dpdf(fn,pf,dd)
        #make_2ddpdf(fn,pf,dd)
        #make_1dpdf(fn,pf,dd)
        #get_stats(fn,pf,dd,fout)
        #get_power(fn,pf,dd,fout)
        get_chem(dire,fn,pf,dd,fout,cs[i],j21[i])
    #move_stuff()

if __name__ == '__main__':
    main()
