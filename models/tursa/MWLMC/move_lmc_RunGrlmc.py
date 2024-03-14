"""
Transform the LMC to an offset position

TODO
decide on a naming system for the outputs based on the offsets

"""

import numpy as np

def rotate_general_vector(A,xrotation,yrotation,zrotation):
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
    return xout,yout,zout


def rotate_lmc_vector(A,lmc_i = 26,lmc_theta = 149):
    x,y,z = A
    radfac = np.pi/180.
    # set rotation in radians
    # LMC orientation from Choi et al 2018 https://arxiv.org/abs/1804.07765
    # rotation matrices given in van der Marel et al 2002 and implemented further below
    theta_LMC = lmc_theta*radfac
    i_LMC = lmc_i*radfac
    Rmatrix = np.array([[np.cos(theta_LMC), -np.sin(theta_LMC) * np.cos(i_LMC), -np.sin(theta_LMC) * np.sin(i_LMC)],
                      [np.sin(theta_LMC), np.cos(theta_LMC) * np.cos(i_LMC), np.cos(theta_LMC) * np.sin(i_LMC)],
                      [0, -np.sin(i_LMC), np.cos(i_LMC)]])
    # structure the points for rotation
    pts = np.array([x,y,z])
    #
    # do the transformation in position
    tmp = np.dot(pts.T,Rmatrix)
    xout = tmp[0]
    yout = tmp[1]
    zout = tmp[2]
    #
    return xout,yout,zout


# set up the ICs for the centre of the halo
dx  = 0.63
dy  = 3.23
dz  = -1.62
dvx = -0.28
dvy = -1.78
dvz = 0.55

for infile in ['/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/halo.250M.bods.diag','/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/disc.5M.bods.diag']:
    g = open(infile,'r')
    nbodies = int(g.readline().split()[0])
    f = open('transformed{}_RunGrlmc.bods'.format(infile.split('/')[-1].split('.')[0]),'w')
    print('{} 0 0'.format(nbodies),file=f)
    for i in range(0,nbodies):
        h = g.readline().split()
        xtmp,ytmp,ztmp = rotate_lmc_vector([float(h[1]),float(h[2]),float(h[3])])
        utmp,vtmp,wtmp = rotate_lmc_vector([float(h[4]),float(h[5]),float(h[6])])
        print(float(h[0]),xtmp+dx,ytmp+dy,ztmp+dz,utmp+dvx,vtmp+dvy,wtmp+dvz,file=f)
    f.close()
    
