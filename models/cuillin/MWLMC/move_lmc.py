"""
Transform the LMC to an offset position

TODO
decide on a naming system for the outputs based on the offsets

"""

import numpy as np
from exptool.io import particle

# set up the ICs for the centre of the halo
dx  = 0.0
dy  = 2.0
dz  = 1.0
dvx = 0.0
dvy = -1.0
dvz = -0.5

from exptool.observables import transform


for comp in ['lmcdisc','lmchalo']:
    I = particle.Input('OUT.runlmc0.00000',comp)
    nbodies = I.header[comp]['nbodies']
    # add the translation
    newx,newy,newz = I.data['x']+dx,I.data['y']+dy,I.data['z']+dz
    newvx,newvy,newvz = I.data['vx']+dvx,I.data['vy']+dvy,I.data['vz']+dvz
    # also do the rotation here: all particles at once.
    f = open('transformed{}.bods'.format(comp),'w')
    print('{} 0 0'.format(nbodies),file=f)
    for i in range(0,nbodies):
        print(I.data['m'][i],newx[i],newy[i],newz[i],newvx[i],newvy[i],newvz[i],file=f)
    f.close()
