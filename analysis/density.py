#%% 
# import packages

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
pwd = os.getcwd()
os.chdir('/Users/slill/Code/EXP/build/pyEXP/')
# print(os.getcwd())
import time
import pyEXP
os.chdir(pwd)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import seaborn as sns   

plt.style.use('my_latex_standard2')


datadir = '/Users/slill/Documents/Projects/exp-extreme-MWLMC/data/extreme-mwlmc'
datadir_mssa = '/Users/slill/Documents/Projects/exp-extreme-MWLMC/data/mssa'

# %%
virialradius=122.0
virialvelocity=119.
massscale = virialvelocity**2 * virialradius / 0.0000043009125  


# %%
# config each component
runtag='RunG5'

## haloes
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
mwhcoefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.{mwhruntag}')


## discs
### MW disc
print("config MW Disc")
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
    rnum       : 200 
    pnum       : 1 
    tnum       : 80 
    vflag      : 16 
    logr       : true 
    self_consistent: true
    cachename  : {datadir}/MWeofhires
# """

mwdruntag = f'mwdisk.{runtag}'
mwdbasis = pyEXP.basis.Basis.factory(mwdconfig)
mwdcoefs = pyEXP.coefs.Coefs.factory(f'{datadir}/outcoef.{mwdruntag}')


#%%
# load orient files 
def read_orient(infile):
    O = np.genfromtxt(infile,skip_header=3)
    t = O[:,0]
    x = O[:,15]
    y = O[:,16]
    z = O[:,17]
    if "disk" in infile or "disc" in infile:
        xangle = O[:,6]
        yangle = O[:,7]
        zangle = O[:,8]
        phi = np.arctan2(yangle,xangle)
        theta = -np.arccos(zangle/np.sqrt(xangle**2 + yangle**2 + zangle**2))
        psi = 0.0
        return {
            't': t, 
            'x': x, 
            'y': y, 
            'z': z, 
            'xangle': xangle, 
            'yangle': yangle, 
            'zangle': zangle, 
            'phi': phi, 
            'theta': theta, 
            'psi': psi
        }
    else:
        return {'t': t, 'x': x, 'y': y, 'z': z}

mwhcenter = read_orient(f'{datadir}/mwhalo.orient.{runtag}')
lmchcenter = read_orient(f'{datadir}/lmchalo.orient.{runtag}')
mwdcenter = read_orient(f'{datadir}/mwdisc.orient.{runtag}')
lmcdcenter = read_orient(f'{datadir}/lmcdisc.orient.{runtag}')

virialradius=122.0
virialvelocity=119.
massscale = virialvelocity**2 * virialradius / 0.0000043009125  

# %%
size = 1./virialradius
npix = 64

times = mwhcoefs.Times()
pmin  = [0.0, -size,  -size]
pmax  = [0.0, size, size]
grid  = [ 0,  npix,  npix]

# make MW fields (LMC fields are shifted by its center at each time step in the for loop)
fields = pyEXP.field.FieldGenerator(times, pmin, pmax, grid)
mwhsurfaces = fields.slices(mwhbasis, mwhcoefs)

mwhkeys = list(mwhsurfaces.keys())
nx = mwhsurfaces[mwhkeys[0]]['dens'].shape[0]
ny = mwhsurfaces[mwhkeys[0]]['dens'].shape[1]


# Make the mesh
x = np.linspace(pmin[1], pmax[1], nx)
y = np.linspace(pmin[2], pmax[2], ny)
xv, yv = np.meshgrid(x, y)


# Frame counter
icnt = 0
cmap = sns.color_palette("rocket", as_cmap=True)


N = cmap.N
cmap.set_under(cmap(1))
cmap.set_over(cmap(N-1))
densmin = 1e5
densmax = 1
vmin=1e8
vmax=5e9
levels = np.logspace(8,9.5,endpoint=True,num=9)

# Iterate through the keys
for time in mwhkeys:
    if time == 0.0: continue
    # time=1.76
    if time > 1.8: break # stop shortly past pericentre
    # if os.path.isfile(f'movies/mwlmchaloes/{runtag}_movie_{icnt:04d}_xz.png'):
    #     icnt += 1
    #     continue
    tmask = mwhcenter['t'] == time
    if sum(tmask) > 1: 
        tmask[np.where(tmask)[0][1:]]=False
    mwhcenter_tmp = np.array([mwhcenter['x'][tmask], mwhcenter['y'][tmask], mwhcenter['z'][tmask]])


    # fig, ax = plt.subplots(1, 1, figsize=(12,10))
    fig, ax0 = plt.subplots(figsize=(6, 4))

    
    mwhmat = mwhsurfaces[time]['dens'] * massscale / pow(virialradius,3)
    
    ax0.set_title('T={:4.3f} [vir]'.format(time))


    # MW density
    cont1 = ax0.contour(xv*virialradius, yv*virialradius, mwhmat.transpose(), levels, norm=colors.LogNorm(), cmap=plt.cm.Greys_r)
    cont2 = ax0.pcolormesh(xv*virialradius, yv*virialradius, mwhmat.transpose(),norm=colors.LogNorm(vmin=vmin, vmax=vmax)) #locator=ticker.LogLocator()    
    ax0.set_aspect('equal')
    ax0.text(0.95, 0.925, 'MW', horizontalalignment='right', verticalalignment='center', transform=ax0.transAxes, c= 'white', fontsize = 16)
    ax0.set_xlabel("$x$ [kpc]")
    ax0.set_ylabel("$z$ [kpc]")
    ax0.invert_xaxis()
    ax0.set_facecolor('k')
    
    cbar = fig.colorbar(cont2, ax=ax0, extend='both')
    cbar.set_label('Density [M$_\odot$ kpc$^{-3}$]')
    cbar.add_lines(cont1)
    
    # save and continue
    fig.savefig(f'movies/innerMW/{runtag}_movie_{icnt:04d}_xz.png', dpi=256, bbox_inches='tight')
    if icnt < 2:
        plt.show()
    else:
        plt.close()

    icnt += 1
    # break
    
    

# %%
import cv2 as cv
import glob
import re

### this function sorts your input files numerically (0,1,,...9,10,11...99, 100,...)
def sorted_nicely( l ):
    """Sorts the given iterable in the way that is expected.
        Required arguments:
        l -- The iterable to be sorted
    """

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)
    
### prepare file list and load images
    
# read in files
files = [f for f in glob.glob(f'./movies/innerMW/{runtag}*.png', recursive=True)] # images saved as png
files = sorted_nicely(files)

files = files[624:]

img = cv.imread(cv.samples.findFile(files[0]))
rows, cols = img.shape[:2]


fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(f'movies/innerMW_{runtag}_yz.mp4', fourcc, 20.0, (cols, rows))
out2 = cv.VideoWriter(f'movies/innerMW_{runtag}_yz.avi', fourcc, 20.0, (cols, rows))

for file in files:
    img = cv.imread(cv.samples.findFile(file))
    rows, cols = img.shape[:2]
    out.write(img)
    out2.write(img)
     
out.release() 
out2.release() 
     

# %%
