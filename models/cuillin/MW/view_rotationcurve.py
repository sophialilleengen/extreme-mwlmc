
# python3.11

import numpy as np
import matplotlib.pyplot as plt

import os
pwd = os.getcwd()
os.chdir('/Users/mpetersen/Code/EXP/build/pyEXP/')
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
  modelname : ../Einasto_rs0.07_rhos24.913_alpha0.16_rtrunc20.txt
  cachename : EinastoR20
"""
halobasis = pyEXP.basis.Basis.factory(hconfig)
halocoefs = pyEXP.coefs.Coefs.factory('../outcoef.mwhalo0b')



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
discbasis = pyEXP.basis.Basis.factory(dconfig)
disccoefs = pyEXP.coefs.Coefs.factory('../outcoef.mwdisk0b')

# make a slice at the first time
times = disccoefs.Times()[0:1]
pmin  = [ 0.0,  0.0, 0.0]
pmax  = [ 1.0,  0.0, 0.0]
grid  = [1000,   1,   0]
rvals = np.linspace(pmin[0],pmax[0],grid[0])

fields = pyEXP.field.FieldGenerator(times, pmin, pmax, grid)

halosurfaces = fields.slices(halobasis, halocoefs)
discsurfaces = fields.slices(discbasis, disccoefs)

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
plt.savefig('/Users/mpetersen/Downloads/rotation_curve_mw.png',dpi=300)


