

# %%
# import things

import os
os.environ["OMP_NUM_THREADS"] = "4" # export OMP_NUM_THREADS=4
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# pwd = os.getcwd()
# os.chdir('/Users/slill/Code/EXP/build/pyEXP/')
# print(os.getcwd())

import time
import pyEXP
# os.chdir(pwd)


# os.chdir('/Users/slill/Documents/Projects/exp-extreme-MWLMC/extreme-mwlmc/analysis/')

print(os.getcwd())
print(pyEXP.util.getVersionInfo())

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import seaborn as sns   

# plt.style.use('my_latex_standard2')


datadir = '/cosma8/data/dp309/dc-lill1/'
datadir_mssa = '/cosma8/data/dp309/dc-lill1/mssa'

datadir='/cosma5/data/durham/dc-lill1/extreme-mwlmc/'
datadir_mssa = '/cosma5/data/durham/dc-lill1/extreme-mwlmc/'
runtag = 'RunG5'
runtag2 = 'newG5'

# %%
virialradius=122.0
virialvelocity=119.
massscale = virialvelocity**2 * virialradius / 0.0000043009125  



# %%
# MW halo coefs
mwhalo_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.mwhalo.{runtag2}')
mwhalo_keylst = mwhalo_coefs.makeKeys([])


# MW disc coefs
mwdisc_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.mwdisk.{runtag}')
mwdisc_keylst = mwdisc_coefs.makeKeys([])

# LMC halo coefs
lmchalo_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.lmchalo.{runtag2}')
lmchalo_coefs2 = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.lmchalo.{runtag2}')
lmchalo_keylst = lmchalo_coefs.makeKeys([])

# LMC disc coefs
lmcdisc_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.lmc.{runtag2}')
# lmcdisc_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.lmcdisk.{runtag}')
lmcdisc_keylst = lmcdisc_coefs.makeKeys([])


# %%
### MW halo
print("config MW halo")
mwhconfig = """
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

mwhruntag = f'mwhalo.{runtag}'
mwhbasis = pyEXP.basis.Basis.factory(mwhconfig)

# %%
### LMC halo
print("config LMC halo")
lmchconfig = """
---
id: sphereSL
parameters :
  numr     : 2000
  rmin     : 0.00001
  rmax     : 2.0
  Lmax     : 6
  nmax     : 20
  rmapping : 0.0667
  modelname : ./Einasto_rs0.035_rhos24.682_alpha0.16_rtrunc33.txt
  cachename : EinastoR33
"""

lmchruntag = f'lmchalo.{runtag}'
lmchbasis = pyEXP.basis.Basis.factory(lmchconfig)

# %%
fname = f'{datadir}/MWeofcachenew'
print(fname)

print(f'MWeofcachenew path works? {os.path.isfile(fname)}')

fname2 = f'{datadir}/LMCeofcachenew'
print(fname2)
print(f'LMCeofcachenew path works? {os.path.isfile(fname2)}')

# %%
### MW disc
print("config MW disc")

mwdconfig=f"""
id         : cylinder
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
  cachename  : {datadir}/MWeofcachenew
"""
disc_basis = pyEXP.basis.Basis.factory(mwdconfig)

# %%
### LMC disc
print("config LMC Disc")

lmcdconfig=f"""
id         : cylinder
parameters :
    acyl       : 0.014
    hcyl       : 0.003
    lmaxfid    : 72
    mmax       : 6
    nmaxfid    : 32
    nmax       : 20
    ncylodd    : 8
    ncylnx     : 256
    ncylny     : 128
    rcylmin    : 0.001
    rcylmax    : 200.0
    cachename  : {datadir}/LMCeofcachenew
"""
#   #cachename  : {datadir}/LMCeofcache
# cachename  : {datadir}/LMCeofcachenew
# rnum       : 200 
# pnum       : 1 
# tnum       : 80 
# vflag      : 16 
# logr       : true 
# self_consistent : true

lmcdruntag = f'lmcdisk.{runtag}'
lmcdbasis = pyEXP.basis.Basis.factory(lmcdconfig)




# %%
### mSSA
# Make some parameter flags as YAML.  The defaults should work fine
# for most people.  'chatty' turns on std::out diagnostics and
# 'output' is the prefix for written files.
#
flags ="""
---
# chatty: on

output: fulltest_default
...
"""


# %%
# more entries here: MW halo MW disc, LMC halo LMC disc; each with coeffs and keylists; made keylist MW: m=6, disc m=4; LMC to 6 in both)
config = {
    "MW halo": (mwhalo_coefs, mwhalo_keylst, []),
        #   "MW disc": (mwdisc_coefs, mwdisc_keylst, []),
          # "LMC halo": (lmchalo_coefs, lmchalo_keylst, []),
        #   "LMC disc": (lmcdisc_coefs, lmcdisc_keylst, [])
          } 

window = int(len(mwhalo_coefs.Times())/2)
npc = 100 # number of principal components; probably want more than 20; max number of PCs would be the window length


# # %%
# %%
print("Window={} PC number={}".format(window, npc))

startTime = time.time()
ssa = pyEXP.mssa.expMSSA(config, window, npc, flags)


# # %%

# ev = ssa.eigenvalues() # do the decomposition (expensive step)
# print('Computed eigenvalues in {:6.2f} seconds'.format(time.time() - startTime))


# # %%
# cum = ssa.cumulative()
# cum



