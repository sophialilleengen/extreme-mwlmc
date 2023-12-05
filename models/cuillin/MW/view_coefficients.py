
# python3.11

import numpy as np
import matplotlib.pyplot as plt

import os
pwd = os.getcwd()
os.chdir('/Users/mpetersen/Code/EXP/build/pyEXP/')
#os.chdir('/home/mpetersen/EXP/build/pyEXP')
import pyEXP
os.chdir(pwd)

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

C = halocoefs.getAllCoefs()

plt.plot(halocoefs.Times(),C[0,0,:])
plt.xlabel('time')
plt.ylabel('coefficient')
plt.tight_layout()
plt.savefig('coefficient_value.png',dpi=300)





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


