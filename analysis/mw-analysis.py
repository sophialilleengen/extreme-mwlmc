# %%
# import things

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
pwd = os.getcwd()
os.chdir('/Users/slill/Code/EXP/build/pyEXP/')
# print(os.getcwd())
import pyEXP
os.chdir(pwd)


import numpy as np
import matplotlib.pyplot as plt
datadir = '/Users/slill/Documents/Projects/exp-extreme-MWLMC/data/extreme-mwlmc'


# %%
# make halo basis and load halo coefficients

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
halocoefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.mwhalo.RunGGG')


# %%
# make disc basis and load disc coefficients
dconfig=f"""
id         : cylinder
parameters :
  acyl       : 0.029
  hcyl       : 0.004
  lmaxfid    : 72
  mmax       : 4
  nmaxfid    : 32
  nmax       : 10
  ncylodd    : 4
  ncylnx     : 512
  ncylny     : 256
  rcylmin    : 0.001
  rcylmax    : 100.0
  cachename  : {datadir}/MWeofcache
"""

discbasis = pyEXP.basis.Basis.factory(dconfig)
disccoefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.mwdisk.RunGGG')

# %%
# plot densities / potential / forces

# %%
# plot coefficients

# %%
# run mssa

# %% 
# plot mssa evaluation plots 


