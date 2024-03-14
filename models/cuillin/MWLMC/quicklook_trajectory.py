
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py runtag")
    sys.exit(1)

# Access the command-line argument
runtag = sys.argv[1]


indir = './'
outdir = './'



def read_orient(infile):
    O = np.genfromtxt(infile,skip_header=3)
    t = O[:,0]
    x = O[:,15]
    y = O[:,16]
    z = O[:,17]
    return t,x,y,z


def read_orient_angles(infile):
    O = np.genfromtxt(infile,skip_header=3)
    t = O[:,0]
    x = O[:,6]
    y = O[:,7]
    z = O[:,8]
    return t,x,y,z



def process_velocities(t,x,y,z,nsmth=1001,norder=2):
    dt = t[101]-t[100]
    # in case of restarts, make sure all time values are unique
    t,tincreasing = np.unique(t,return_index=True)
    xf = savgol_filter(x[tincreasing], nsmth,norder,deriv=1)/dt
    yf = savgol_filter(y[tincreasing], nsmth,norder,deriv=1)/dt
    zf = savgol_filter(z[tincreasing], nsmth,norder,deriv=1)/dt
    vxfunc = UnivariateSpline(t,xf,s=0)
    vyfunc = UnivariateSpline(t,yf,s=0)
    vzfunc = UnivariateSpline(t,zf,s=0)
    xf = savgol_filter(x[tincreasing], nsmth,norder,deriv=0)
    yf = savgol_filter(y[tincreasing], nsmth,norder,deriv=0)
    zf = savgol_filter(z[tincreasing], nsmth,norder,deriv=0)
    xfunc = UnivariateSpline(t,xf,s=0)
    yfunc = UnivariateSpline(t,yf,s=0)
    zfunc = UnivariateSpline(t,zf,s=0)
    return xfunc,yfunc,zfunc,vxfunc,vyfunc,vzfunc


def compute_relative_positions_velocities_and_print(indir,runtag,comps,fixed_time=-1,tlimit=-1.):
    # first component
    for ic in range(0,len(comps)):
        ofile1 = indir + comps[ic] + '.orient.'+runtag
        t1,x1,y1,z1 = read_orient(ofile1)
        xf1,yf1,zf1,vxf1,vyf1,vzf1 = process_velocities(t1,x1,y1,z1,nsmth=1001,norder=2)
        w = np.where(t1>tlimit)[0]
        f = open(ofile1+'.smth','w')
        print(t1[w].size,file=f)
        for indx in w:#range(0,t1.size):
        #print(t1[indx],x1[indx],y1[indx],z1[indx],vxf1(t1[indx]),vyf1(t1[indx]),vzf1(t1[indx]),file=f)
            print(t1[indx],x1[indx],y1[indx],z1[indx],vxf1(t1[indx]),vyf1(t1[indx]),vzf1(t1[indx]),file=f)
        f.close()



clr = 'black'

compute_relative_positions_velocities_and_print(indir,runtag,['mwhalo','lmchalo','mwdisc','lmcdisc'])


O = dict()
for comp in ['mwhalo','lmchalo','mwdisc','lmcdisc']:
    O[comp] = np.genfromtxt(indir+comp+'.orient.'+runtag+'.smth',skip_header=1)

virialradius=122.0
virialvelocity=119.
nmax = np.nanmin([O['lmcdisc'].shape[0],O['mwdisc'].shape[0]])
lmcdiff = O['lmcdisc'][0:nmax] - O['mwdisc'][0:nmax]
xlmcd = lmcdiff[:,1:4]*virialradius
vlmcd = lmcdiff[:,4:7]*virialvelocity

lmcdiff = O['lmchalo'][0:nmax] - O['mwdisc'][0:nmax]
xlmch = lmcdiff[:,1:4]*virialradius
vlmch = lmcdiff[:,4:7]*virialvelocity

for p in [0,1,2]:
    plt.plot(O['lmcdisc'][0:nmax,0],xlmcd[:,p],color=clr,linestyle='dotted')
    plt.plot(O['lmchalo'][0:nmax,0],xlmch[:,p],color='grey',linestyle='dotted')

plt.plot(O['lmcdisc'][0:nmax,0],np.linalg.norm(xlmcd,axis=1),color=clr)
plt.plot(O['lmchalo'][0:nmax,0],np.linalg.norm(xlmch,axis=1),color='grey')

plt.xlabel('distance')
plt.ylabel('time')
plt.tight_layout()
plt.savefig('trajectory_{}.png'.format(runtag),dpi=300)




# Sophia's
targetx = np.array([-0.61436097, -41.02036742, -26.83297465])
targetv = np.array([-69.85587904, -221.68751413, 214.15271769])

# Mike's
targetx = np.array([ -0.425172   -41.01213084 -26.82899933])
targetv = np.array([ -54.62928797  -208.98991061 198.85436269])


for runtag in ['RunA','RunD','RunH','RunI','RunJ','RunK','RunL','RunM','RunN','RunO','RunP','RunQ','RunR','RunS','RunT','RunU']:
    O = dict()
    for comp in ['mwhalo','lmchalo','mwdisc','lmcdisc']:
        O[comp] = np.genfromtxt(indir+comp+'.orient.'+runtag+'.smth',skip_header=1)
    virialradius=122.0
    virialvelocity=119.
    nmax = np.nanmin([O['lmcdisc'].shape[0],O['mwdisc'].shape[0]])
    lmcdiff = O['lmcdisc'][0:nmax] - O['mwdisc'][0:nmax]
    xlmcd = lmcdiff[:,1:4]*virialradius
    vlmcd = lmcdiff[:,4:7]*virialvelocity
    sigmax = 1.0
    sigmav = 10.0
    xdiff = np.linalg.norm((xlmcd-targetx)/sigmax,axis=1)
    vdiff = np.linalg.norm((vlmcd-targetv)/sigmav,axis=1)
    bestval = np.nanargmin(xdiff[0:nmax]+vdiff[0:nmax])
    print(runtag,np.nanmin(xdiff[0:nmax]+vdiff[0:nmax]))
    print(O['lmcdisc'][bestval,0])
    print(xlmcd[bestval],np.linalg.norm(xlmcd[bestval]))
    print(vlmcd[bestval],np.linalg.norm(vlmcd[bestval]))
    print(xlmcd[0]/virialradius,np.linalg.norm(xlmcd[0]/virialradius))
    print(vlmcd[0]/virialvelocity,np.linalg.norm(vlmcd[0]/virialvelocity))
    print('------------------------------------')


"""
for p in [0,1,2]:
    plt.plot(O['lmcdisc'][0:nmax,0],vlmc[:,p],color=clr)

plt.plot(O['lmc'][0:nmax,0],np.linalg.norm(vlmc,axis=1),color=clr)


btime = 1.75
btimeindx = np.nanargmin(np.abs(O['lmc'][0:nmax,0]-btime))
print(xlmc[btimeindx])
print(vlmc[btimeindx])
np.linalg.norm(xlmc[btimeindx])
np.linalg.norm(vlmc[btimeindx])
"""