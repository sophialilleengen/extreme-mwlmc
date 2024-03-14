"""
Transform the LMC to an offset position

TODO
decide on a naming system for the outputs based on the offsets

"""

import numpy as np
from exptool.io import particle


from exptool.observables import transform

comp = 'mwdisc'

I = particle.Input('MW0/OUT.runmw0.00000',comp,legacy=True)
nbodies = I.header[comp]['nbodies']

I = particle.Input('MWLMC0/OUT.RunGo.00000',comp,legacy=True)
nbodies = I.header[comp]['nbodies']
print(np.nanmax(np.abs(I.xpos)),np.nanmax(np.abs(I.zpos)))


# this rotation brings the disc to the x-z plane
O = transform.rotate_points(I,90.,0.,0.)
# verify that the twist worked
print(np.nanmax(np.abs(O.xpos)),np.nanmax(np.abs(O.ypos)))

newx,newy,newz = transform.rotate_point_vector([I.xpos,I.ypos,I.zpos],90.,0.,0.)
transform.rotate_point_vector([I.xpos[0],I.ypos[0],I.zpos[0]],90.,0.,0.)


# this rotation brings the disc to the y-z plane
O = transform.rotate_points(I,90.,0.,90.)
# verify that the twist worked
print(np.nanmax(np.abs(O.xpos)),np.nanmax(np.abs(O.ypos)))


# also do the rotation here: all particles at once.
newx,newy,newz = O.xpos,O.ypos,O.zpos
newvx,newvy,newvz = O.xvel,O.yvel,O.zvel
# add the translation

f = open('MW0/transformed{}.bods'.format(comp),'w')
print('{} 0 0'.format(nbodies),file=f)
for i in range(0,nbodies):
    print(I.mass[i],newx[i],newy[i],newz[i],newvx[i],newvy[i],newvz[i],file=f)
f.close()

def rotate_point_vector(A,xrotation,yrotation,zrotation):
    x,y,z = A
    radfac = np.pi/180.
    # set rotation in radians
    a = xrotation*radfac # xrotation (the tip into/out of page)
    b = yrotation*radfac # yrotation
    c = zrotation*radfac # zrotation
    # construct the rotation matrix TAIT-BRYAN method (x-y-z,
    # extrinsic rotations)
    Rx = np.array([[1.,0.,0.],[0.,np.cos(a),np.sin(a)],[0.,-np.sin(a),np.cos(a)]])
    Ry = np.array([[np.cos(b),0.,-np.sin(b)],[0.,1.,0.],[np.sin(b),0.,np.cos(b)]])
    Rz = np.array([[np.cos(c),np.sin(c),0.,],[-np.sin(c),np.cos(c),0.],[0.,0.,1.]])
    Rmatrix = np.dot(Rx,np.dot(Ry,Rz))
    # structure the points for rotation
    pts = np.array([x,y,z])
    #
    # do the transformation in position
    tmp = np.dot(pts.T,Rmatrix)
    xout = tmp[0]
    yout = tmp[1]
    zout = tmp[2]
    #
    return [xout,yout,zout]

rotate_point_vector([I.xpos[0],I.ypos[0],I.zpos[0]],90.,0.,0.)
