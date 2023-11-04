"""
Transform the LMC to an offset position

TODO
decide on a naming system for the outputs based on the offsets

"""

import numpy as np
from exptool.io import particle

from exptool.observables import transform

comp = 'mwdisc'

I = particle.Input('OUT.runmw0.00000',comp,legacy=True)
nbodies = I.header[comp]['nbodies']

# this rotation brings the disc to the x-z plane
O = transform.rotate_points(PSPDump,90.,0.,0.)

# also do the rotation here: all particles at once.
newx,newy,newz = O.xpos,O.ypos,O.zpos
newvx,newvy,newvz = O.xvel,O.yvel,O.zvel
# add the translation

f = open('transformed{}.bods'.format(comp),'w')
print('{} 0 0'.format(nbodies),file=f)
for i in range(0,nbodies):
    print(I.data['m'][i],newx[i],newy[i],newz[i],newvx[i],newvy[i],newvz[i],file=f)
f.close()
