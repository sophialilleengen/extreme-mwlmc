import numpy as np
from scipy import special

# choose the Einasto parameters of interest (rounded)
rsphysical    = 4.25 # kpc
rhosphysical  = 8.56e6 # Msun/kpc^3
alpha         = 0.16
rtruncfactor  = 25    # how many scale radii should we apply a rolloff?

# convert to G=1 units
astronomicalG = 0.0000043009125 # gravitational constant, (km/s)^2 * kpc / Msun
rvir          = 122. # kpc
vvir          = 149. # km/s (circular velocity at virial radius)
mvir          = vvir * vvir * rvir / astronomicalG
print('virial mass is {}'.format(mvir))

rs            = np.round(rsphysical/rvir,3)
rhos          = np.round(rhosphysical * np.power(rvir,3) / mvir,3)
print('virial density is {}'.format(rhos))


def makemodel(func,M,funcargs,rvals = 10.**np.linspace(-2.,4.,2000),pfile='',plabel = '',verbose=True):
    """make an EXP-compatible spherical basis function table

    inputs
    -------------
    func        : (function) the callable functional form of the density
    M           : (float) the total mass of the model, sets normalisations
    funcargs    : (list) a list of arguments for the density function.
    rvals       : (array of floats) radius values to evaluate the density function
    pfile       : (string) the name of the output file. If '', will not print file
    plabel      : (string) comment string
    verbose     : (boolean)

    outputs
    -------------
    R           : (array of floats) the radius values
    D           : (array of floats) the density
    M           : (array of floats) the mass enclosed
    P           : (array of floats) the potential

    """

    R = np.nanmax(rvals)

    # query out the density values
    dvals = func(rvals,*funcargs)

    # make the mass and potential arrays
    mvals = np.zeros(dvals.size)
    pvals = np.zeros(dvals.size)
    pwvals = np.zeros(dvals.size)

    # initialise the mass enclosed an potential energy
    mvals[0] = 1.e-15
    pwvals[0] = 0.

    # evaluate mass enclosed and potential energy by recursion
    for indx in range(1,dvals.size):
        mvals[indx] = mvals[indx-1] +\
          2.0*np.pi*(rvals[indx-1]*rvals[indx-1]*dvals[indx-1] +\
                 rvals[indx]*rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);
        pwvals[indx] = pwvals[indx-1] + \
          2.0*np.pi*(rvals[indx-1]*dvals[indx-1] + rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);

    # evaluate potential (see theory document)
    pvals = -mvals/(rvals+1.e-10) - (pwvals[dvals.size-1] - pwvals)

    # get the maximum mass and maximum radius
    M0 = mvals[dvals.size-1]
    R0 = rvals[dvals.size-1]

    # compute scaling factors
    Beta = (M/M0) * (R0/R);
    Gamma = np.sqrt((M0*R0)/(M*R)) * (R0/R);
    if verbose:
        print("! Scaling:  R=",R,"  M=",M)

    rfac = np.power(Beta,-0.25) * np.power(Gamma,-0.5);
    dfac = np.power(Beta,1.5) * Gamma;
    mfac = np.power(Beta,0.75) * np.power(Gamma,-0.5);
    pfac = Beta;

    if verbose:
        print(rfac,dfac,mfac,pfac)

    # save file if desired
    if pfile != '':
        f = open(pfile,'w')
        print('! ',plabel,file=f)
        print('! R    D    M    P',file=f)

        print(rvals.size,file=f)

        for indx in range(0,rvals.size):
            print('{0} {1} {2} {3}'.format( rfac*rvals[indx],\
              dfac*dvals[indx],\
              mfac*mvals[indx],\
              pfac*pvals[indx]),file=f)

        f.close()

    return rvals*rfac,dfac*dvals,mfac*mvals,pfac*pvals



def einasto(r,rs=1.,rhos=1.,alpha=1.,rtruncfactor=25):
    """return einasto profile

    """
    ra = r/rs
    dens = rhos * np.exp(-(2/alpha) * (ra**alpha - 1))
    rtrunc = rtruncfactor*rs
    wtrunc = rtrunc*0.2
    rolloff = 0.5 - 0.5*special.erf((r-rtrunc)/wtrunc)
    return dens*rolloff


R,D,M,P = makemodel(einasto,1.0,[rs,rhos,alpha,rtruncfactor],rvals = 10.**np.linspace(-5.,0.3,2000),pfile='Einasto_rs{}_rhos{}_alpha{}_rtrunc{}.txt'.format(rs,rhos,alpha,rtruncfactor),plabel = 'Einasto_rs{}_rhos{}_alpha{}_rtrunc{}.txt'.format(rs,rhos,alpha,rtruncfactor))


def check_concentration(R,D):
    """
    check the  concentration of a halo
    by finding where the power law is most similar to alpha^-2

    return 1./radius, which is the concentration.
    (so find the scale radius by taking 1./concentration)

    """
    func = np.log10(R**-2.)-np.log10(D)
    print('Concentration={}'.format(1./R[np.nanargmin(func)]))



check_concentration(R,D)
print("masscrossing=",M[np.nanargmin(np.abs(R-1.))])
