"""
Test the Orient code for doing rotations.
This code is a facsimile of how Orient works.

Basic sketch:
Using the summed (over all particles) angular momentum vectors,
compute the rotation angles (phi,theta,psi),
construct the rotation matrix,
transform the particles to the rotated frame,
compute the coefficients.
Then, while still in the rotated frame, compute the forces from the basis (how does this work for mixed components?),
before finally rotating back to the original frame.


Pitfalls:
Coefficients time streams, broken down, will be difficult to analyse as they will have a rotation constantly applied

Todo:
Test a rotated run for coefficients; should be very similar to other runs.
Test the vanilla run to see what axis does
Check

Is Orient working on the CPU side? On the GPU side?
There is some strange interval to start before the orientation picks up.

"""

import numpy as np
from exptool.io import particle

from exptool.observables import transform

def return_euler_slater(PHI, THETA, PSI, BODY):
    sph = np.sin(PHI)
    cph = np.cos(PHI)
    sth = np.sin(THETA)
    cth = np.cos(THETA)
    sps = np.sin(PSI)
    cps = np.cos(PSI)
    euler = np.zeros((3, 3))
    euler[0, 0] = -sps * sph + cth * cph * cps
    euler[0, 1] = sps * cph + cth * sph * cps
    euler[0, 2] = cps * sth
    euler[1, 0] = -cps * sph - cth * cph * sps
    euler[1, 1] = cps * cph - cth * sph * sps
    euler[1, 2] = -sps * sth
    euler[2, 0] = -sth * cph
    euler[2, 1] = -sth * sph
    euler[2, 2] = cth
    if BODY:
        return euler.T
    else:
        return euler


comp = 'lmcdisc'

I = particle.Input('../LMC/LMC0/OUT.runlmc0.00000',comp,legacy=True)
nbodies = I.header[comp]['nbodies']

# now let's try to compute the euler angles and see what happens

#I = transform.rotate_points(I,90.,45.,10.)
I = transform.rotate_points(I,90.,0.,0.)

# compute all angular momenta
Lx = I.ypos*I.zvel - I.zpos*I.yvel
Ly = I.zpos*I.xvel - I.xpos*I.zvel
Lz = I.xpos*I.yvel - I.ypos*I.xvel

print(np.nansum(Lx),np.nansum(Ly),np.nansum(Lz))

axis = np.array([np.nansum(Lx),np.nansum(Ly),np.nansum(Lz)])

phi   = np.arctan2(axis[1], axis[0]);
theta = -np.arccos(axis[2]/np.linalg.norm(axis));
psi   = 0.0;
print(phi,theta,psi)

body = return_euler_slater(phi, theta, psi, 0);
orig = return_euler_slater(phi, theta, psi, 1);

# transform these so that Lz is the largest magnitude
pts = np.array([I.xpos,I.ypos,I.zpos])
tmp = np.dot(body,pts)
newx,newy,newz = tmp[0],tmp[1],tmp[2]
pts = np.array([I.xvel,I.yvel,I.zvel])
tmp = np.dot(body,pts)
newu,newv,neww = tmp[0],tmp[1],tmp[2]

newLx = newy*neww - newz*newv
newLy = newz*newx - newu*neww
newLz = newx*newv - newy*newu
print(np.nansum(newLx),np.nansum(newLy),np.nansum(newLz))


# now after the fact, we can take a look at the rotated version
import numpy as np
import matplotlib.pyplot as plt
from exptool.io import particle

comp = 'mwdisc'


runtag = 'runmw0br'
I = particle.Input('OUT.{}.00000'.format(runtag),comp)
I.data['x']

runtag = 'runmw0brcpu'
I = particle.Input('OUT.{}.00000'.format(runtag),comp)
I.data['x']

v2 = I.data['vx']**2 + I.data['vy']**2 + I.data['vz']**2 
tE = np.nansum(v2 + I.data['potE'])
print(tE)



plt.figure()
plt.scatter(I.data['y'][::100],I.data['z'][::100],facecolor='black',edgecolor='none',s=1.)

plt.tight_layout()
plt.savefig('quick_galaxy.png',dpi=300)


I = particle.Input('OUT.{}.00002'.format(runtag),comp)
