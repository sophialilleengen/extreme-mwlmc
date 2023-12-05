"""
Transform the LMC to an offset position

TODO
decide on a naming system for the outputs based on the offsets

"""

import numpy as np
from exptool.io import particle
from exptool.observables import transform


# set up the ICs for the centre of the halo
dx  = {{OFFSETX}}
dy  = {{OFFSETY}}
dz  = {{OFFSETZ}}
dvx = {{OFFSETU}}
dvy = {{OFFSETV}}
dvz = {{OFFSETW}}


for infile in ['../LMC/LMC00/disc.1Ms.bods.diag','../LMC/LMC00/halo.5Ms.bods.diag']:
    g = open(infile,'r')
    nbodies = int(g.readline().split()[0])
    f = open('MWLMC0/transformed{}_{{NAME}}.bods'.format(infile.split('/')[-1].split('.')[0]),'w')
    print('{} 0 0'.format(nbodies),file=f)
    for i in range(0,nbodies):
        h = g.readline().split()
        print(float(h[0]),float(h[1])+dx,float(h[2])+dy,float(h[3])+dz,float(h[4])+dvx,float(h[5])+dvy,float(h[6])+dvz,file=f)
    f.close()
    

"""
runtag = 'runlmc0'

for comp in ['lmcdisc','lmchalo']:
    I = particle.Input('OUT.{}.00000'.format(runtag),comp)
    nbodies = I.header[comp]['nbodies']
    # also do the rotation here: all particles at once.
    #
    # add the translation
    newx,newy,newz = I.data['x']+dx,I.data['y']+dy,I.data['z']+dz
    newvx,newvy,newvz = I.data['vx']+dvx,I.data['vy']+dvy,I.data['vz']+dvz
    f = open('transformed{}.bods'.format(comp),'w')
    print('{} 0 0'.format(nbodies),file=f)
    for i in range(0,nbodies):
        print(I.data['m'][i],newx[i],newy[i],newz[i],newvx[i],newvy[i],newvz[i],file=f)
    f.close()
"""
