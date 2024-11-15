import os
os.environ["OMP_NUM_THREADS"] = "4" # export OMP_NUM_THREADS=4

import time
import pyEXP

print(os.getcwd())
print(pyEXP.util.getVersionInfo())



datadir = '/cosma8/data/dp309/dc-lill1/'
# datadir= './'


# MW halo coefs
mwhalo_coefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.mwhalo.newG5')
mwhalo_keylst = mwhalo_coefs.makeKeys([])

#
flags ="""
---
# chatty: on

output: fulltest_default
...
"""


# %%
config = {
    "MW halo": (mwhalo_coefs, mwhalo_keylst, []),
          } 

window = int(len(mwhalo_coefs.Times())/2)
npc = 100 # number of principal components; probably want more than 20; max number of PCs would be the window length


# # %%
# %%
print("Window={} PC number={}".format(window, npc))

startTime = time.time()
ssa = pyEXP.mssa.expMSSA(config, window, npc, flags)
