# cd /Users/mpetersen/Notebooks/Dynamics/extreme-mwlmc/models/cuillin/MWLMC

# python3.11

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

indir = '/Users/mpetersen/Notebooks/Dynamics/extreme-mwlmc/models/cuillin/MWLMC/coefficients/'
indirtraj = '/Users/mpetersen/Notebooks/Dynamics/extreme-mwlmc/models/cuillin/MWLMC/traj/'

import os
pwd = os.getcwd()
os.chdir('/Users/mpetersen/Code/EXP/build/pyEXP/')
#os.chdir('/home/mpetersen/EXP/build/pyEXP')
import pyEXP
os.chdir(pwd)

runtags = ['RunK']
component = 'mwhalo'
runtag = runtags[0]


runtags = ['RunA','RunI','RunJ','RunK','RunL','RunN','RunO','RunP','RunQ','RunR','RunU','RunW','RunX','RunY']

#runtags = ['RunK']

#keylst = halocoefs.makeKeys([1])
#print("All l=1 keys=", keylst)

# Make some custom [m, n] pairs
#keylst = [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7]]
#print("Custom keys=", keylst)
keylst = [[1, 0, 0], [1, 0, 1], [1, 0, 2], [1, 0, 3], [1, 0, 4],
          [1, 1, 0], [1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 1, 4]]

flags ="""
---
output: run
...
"""

plt.figure()
for irun,runtag in enumerate(runtags):
    clr = cm.viridis(irun/len(runtags))
    O = dict()
    for comp in ['mwhalo','lmchalo','mwdisc','lmcdisc']:
        O[comp] = np.genfromtxt(indirtraj+comp+'.orient.'+runtag+'.smth',skip_header=1)
    virialradius=122.0
    virialvelocity=119.
    nmax = np.nanmin([O['lmcdisc'].shape[0],O['mwdisc'].shape[0]])
    lmcdiff = O['lmcdisc'][0:nmax] - O['mwdisc'][0:nmax]
    xlmcd = lmcdiff[:,1:4]*virialradius
    vlmcd = lmcdiff[:,4:7]*virialvelocity
    sigmax = 1.0
    sigmav = 5.0
    #xdiff = np.linalg.norm((xlmcd-targetx)/sigmax,axis=1)
    #vdiff = np.linalg.norm((vlmcd-targetv)/sigmav,axis=1)
    # peg to pericetre
    bestval = np.nanargmin(np.linalg.norm(xlmcd,axis=1))
    #print(runtag,np.nanmin(xdiff[0:nmax]+vdiff[0:nmax]))
    peritime = O['lmcdisc'][bestval,0]
    peridist = np.nanmin(np.linalg.norm(xlmcd,axis=1))
    perivel = np.linalg.norm(vlmcd,axis=1)[bestval]
    #print(xlmcd[bestval],np.linalg.norm(xlmcd[bestval]))
    #print(vlmcd[bestval],np.linalg.norm(vlmcd[bestval]))
    halocoefs = pyEXP.coefs.Coefs.factory(indir+'outcoef.{}.{}'.format(component,runtag))
    C = halocoefs.getAllCoefs()
    # get a value at pericentre
    l1amplitude = np.nansum(np.linalg.norm(C[1:4,:,:],axis=0),axis=0)
    cperitime = np.nanargmin(np.abs(halocoefs.Times()-peritime))
    print(runtag,peritime,peridist,l1amplitude[cperitime])
    #_ = plt.plot(halocoefs.Times()-peritime,l1amplitude,color=cm.viridis((peridist-30)/50))
    #_ = plt.plot(halocoefs.Times()-peritime,np.nansum(np.linalg.norm(C[4:9,:,:],axis=0),axis=0),color=cm.viridis((peridist-30)/50))
    times = halocoefs.Times()
    shortcoefs = pyEXP.coefs.SphCoefs(False)
    for indx,t in enumerate(times[0:cperitime]):
      # do the false duplication for extra time
      shortcoefs.add(halocoefs.getCoefStruct(t))
    config = {"mwhalo": (shortcoefs, keylst, [])}
    window = int(len(shortcoefs.Times())/2)
    npc = 20
    print("Window={} PC number={}".format(window, npc))
    ssa = pyEXP.mssa.expMSSA(config, window, npc, flags)
    ev = ssa.eigenvalues()
    times = halocoefs.Times()
    pc = ssa.getPC()
    rows, cols = pc.shape
    #plt.plot(times[0:rows]-np.nanmax(times[0:rows]),pc[:,0]*np.sign(pc[-1,0])/np.nanmax(pc[:,0]*np.sign(pc[-1,0])),color='black')
    plt.plot(times[0:rows]-np.nanmax(times[0:rows]),pc[:,0]*np.sign(pc[-1,0]),color='black')
    plt.plot(times[0:rows]-np.nanmax(times[0:rows]),pc[:,1]*np.sign(pc[-1,1]),color='grey')


plt.xlabel('lag time')
plt.ylabel('PC0')
#plt.axis([-1.5,0.1,0.,0.5])
plt.tight_layout()
plt.savefig('/Users/mpetersen/Downloads/coefficient_value.png',dpi=300)
#plt.savefig('/Users/mpetersen/Downloads/coefficient_value.png',dpi=300)





plt.figure()
for irun,runtag in enumerate(runtags):
    clr = cm.viridis(irun/len(runtags))
    O = dict()
    for comp in ['mwhalo','lmchalo','mwdisc','lmcdisc']:
        O[comp] = np.genfromtxt(indirtraj+comp+'.orient.'+runtag+'.smth',skip_header=1)
    virialradius=122.0
    virialvelocity=119.
    nmax = np.nanmin([O['lmcdisc'].shape[0],O['mwdisc'].shape[0]])
    lmcdiff = O['lmcdisc'][0:nmax] - O['mwdisc'][0:nmax]
    xlmcd = lmcdiff[:,1:4]*virialradius
    vlmcd = lmcdiff[:,4:7]*virialvelocity
    sigmax = 1.0
    sigmav = 5.0
    #xdiff = np.linalg.norm((xlmcd-targetx)/sigmax,axis=1)
    #vdiff = np.linalg.norm((vlmcd-targetv)/sigmav,axis=1)
    # peg to pericetre
    bestval = np.nanargmin(np.linalg.norm(xlmcd,axis=1))
    #print(runtag,np.nanmin(xdiff[0:nmax]+vdiff[0:nmax]))
    peritime = O['lmcdisc'][bestval,0]
    peridist = np.nanmin(np.linalg.norm(xlmcd,axis=1))
    perivel = np.linalg.norm(vlmcd,axis=1)[bestval]
    #print(xlmcd[bestval],np.linalg.norm(xlmcd[bestval]))
    #print(vlmcd[bestval],np.linalg.norm(vlmcd[bestval]))
    halocoefs = pyEXP.coefs.Coefs.factory(indir+'outcoef.{}.{}'.format(component,runtag))
    C = halocoefs.getAllCoefs()
    # get a value at pericentre
    l1amplitude = np.nansum(np.linalg.norm(C[1:4,:,:],axis=0),axis=0)
    cperitime = np.nanargmin(np.abs(halocoefs.Times()-peritime))
    print(runtag,peritime,peridist,l1amplitude[cperitime])
    _ = plt.plot(halocoefs.Times()-peritime,l1amplitude,color=cm.viridis((peridist-30)/50))
    #_ = plt.plot(halocoefs.Times()-peritime,np.nansum(np.linalg.norm(C[4:9,:,:],axis=0),axis=0),color=cm.viridis((peridist-30)/50))

plt.xlabel('lag time')
plt.ylabel('PC0')
#plt.axis([-1.5,0.1,0.,0.5])
plt.tight_layout()
plt.savefig('/Users/mpetersen/Downloads/coefficient_value_l1.png',dpi=300)
#plt.savefig('/Users/mpetersen/Downloads/coefficient_value.png',dpi=300)


# 
#    
#plt.xlabel('time')
#plt.ylabel('l=1 coefficient')
#plt.axis([-1.5,0.1,0.,0.5])
#plt.tight_layout()
#plt.savefig('/Users/mpetersen/Downloads/coefficient_value.png',dpi=300)




rows, cols = pc.shape

for i in range(min(cols,4)):
    plt.plot(times[0:rows], pc[:,i], '-', label="{:d}".format(i))

plt.xlabel('Time')
plt.ylabel('PC')
plt.legend()
plt.title("Principal components (left-singular vectors)")
plt.show(block=False)






hconfig = """
---
id: sphereSL
parameters :
  numr     : 2000
  rmin     : 0.00001
  rmax     : 2.0
  Lmax     : 6
  nmax     : 20
  rmapping : 0.0667
  modelname : Einasto_rs0.07_rhos24.913_alpha0.16_rtrunc20.txt
  cachename : EinastoR20
"""
halobasis = pyEXP.basis.Basis.factory(hconfig)
halocoefs = pyEXP.coefs.Coefs.factory('outcoef.mwhalo0b')
halocoefs = pyEXP.coefs.Coefs.factory('outcoef.mwhalo0c')


dconfig = """
id : cylinder
parameters :
  acyl       : 0.029
  hcyl       : 0.004
  lmaxfid    : 72
  mmax       : 6
  nmaxfid    : 32
  nmax       : 20
  ncylodd    : 8
  ncylnx     : 256
  ncylny     : 128
  rcylmin    : 0.001
  rcylmax    : 20.0
  rnum       : 200
  pnum       : 1
  tnum       : 80
  vflag      : 16
  logr       : true
  eof_file   : ../.MWeof
"""
dconfig = """
id : cylinder
parameters :
  acyl       : 0.029
  hcyl       : 0.004
  lmaxfid    : 72
  mmax       : 6
  nmaxfid    : 32
  nmax       : 20
  ncylodd    : 8
  ncylnx     : 512
  ncylny     : 256
  rcylmin    : 0.001
  rcylmax    : 100.0
  rnum       : 200
  pnum       : 1
  tnum       : 80
  vflag      : 16
  logr       : true
  eof_file   : .MWeofhires
"""
discbasis = pyEXP.basis.Basis.factory(dconfig)
disccoefs = pyEXP.coefs.Coefs.factory('outcoef.mwdisk0b')
disccoefs = pyEXP.coefs.Coefs.factory('outcoef.mwdisk0c')


disccoefs = pyEXP.coefs.Coefs.factory('outcoef.mwdisk0000')
disccoefs = pyEXP.coefs.Coefs.factory('outcoef.mwdisk00')

disccoefs = pyEXP.coefs.Coefs.factory('../../cuillin/MW/outcoef.mwdisk0')

C = disccoefs.getAllCoefs()

plt.plot(disccoefs.Times(),np.abs(C[2,0,:]))

norm = np.linalg.norm(np.abs(C[0,:,:]),axis=0)
plt.plot(disccoefs.Times(),np.log10(np.linalg.norm(np.abs(C[2,:,:])/norm,axis=0)))
plt.xlabel('time')
plt.ylabel('coefficient')
plt.tight_layout()
plt.savefig('coefficient_value.png',dpi=300)


disccoefs = pyEXP.coefs.Coefs.factory('../../cuillin/LMC/LMC00/outcoef.lmcdisk000')
C = disccoefs.getAllCoefs()

#plt.plot(disccoefs.Times(),np.abs(C[2,0,:]))

norm = np.linalg.norm(np.abs(C[0,:,:]),axis=0)
plt.plot(disccoefs.Times(),np.log10(np.linalg.norm(np.abs(C[1,:,:])/norm,axis=0)))
#plt.plot(disccoefs.Times(),norm)
plt.xlabel('time')
plt.ylabel('coefficient')
plt.tight_layout()
plt.savefig('coefficient_value.png',dpi=300)





# >>> discsurfaces[0.0].keys()
# dict_keys(['azi force', 'dens', 'dens m=0', 'dens m>0', 'mer force', 'potl', 'potl m=0', 'potl m>0', 'rad force'])

vcdisc = np.sqrt(rvals*-discsurfaces[0.0]['rad force'][:,0])
vchalo = np.sqrt(rvals*-halosurfaces[0.0]['rad force'][:,0])
vctotal = np.sqrt(rvals*-(discsurfaces[0.0]['rad force']+halosurfaces[0.0]['rad force'])[:,0])

plt.figure(figsize=(4,3))

rvir,vvir = 122,149

plt.plot(rvir*rvals,vvir*vcdisc,linestyle='dotted',color='black')
plt.plot(rvir*rvals,vvir*vchalo,linestyle='dashed',color='black')
plt.plot(rvir*rvals,vvir*vctotal,color='black')

plt.xlabel('radius (kpc)')
plt.ylabel('velocity (km/s)')
plt.tight_layout()
plt.savefig('rotation_curve_mw_c.png',dpi=300)


