


import numpy as np
import matplotlib.pyplot as plt

def read_outlog(filename):
    """definition to read EXP 'OUTLOG'-style files
    One large dictionary is returned, with sub-dictionaries.
    Each component is returned as a sub-dictionary, with positions,
      velocities, and energy conservation.
    An additional sub-dictionary, with global quantities, is also included.
    """
    # each orbit has various quantities printed:
    global_columns = ['time','mass','bodies','x','y','z','u','v','w','Lx','Ly','Lz','KE','PE','VC','E','2T/VC','clock','used']
    component_columns = ['mass','bodies','x','y','z','u','v','w','Lx','Ly','Lz','Cx','Cy','Cz','KE','PE','VC','E','2T/VC','used']
    # open the file once to see the structure
    A = np.genfromtxt(filename,skip_header=6,delimiter='|')
    # how many entries are there in the first row?
    columns = A.shape[1]
    # compute the number of components
    n_components = int((columns-19)/20)
    # go back and prepare to get the component names
    B = np.genfromtxt(filename,skip_header=2,comments="@",delimiter='|',dtype='S20', invalid_raise=False)
    Log = dict()
    # first read in the global component
    Log['global'] = dict()
    for ikey,key in enumerate(global_columns):
            Log['global'][key] = A[:,ikey]
    for component in range(n_components):
        # get the correct component name
        st = B[0][20*component+19].split()
        if len(st)>1:
            st = [s.decode() for s in st[0:-1]]
            component_name = ' '.join(st)
        else:
            component_name = st[0].decode()
        Log[component_name] = dict()
        for ikey,key in enumerate(component_columns):
            Log[component_name][key] = A[:,20*component+ikey+19]
    return Log


import matplotlib.pyplot as plt

comp = 'mwdisc'
O = read_outlog('OUTLOG.runmw0brcpu')
plt.plot(O['global']['time'],O[comp]['E'],color='black')
plt.savefig('/Users/mpetersen/Downloads/tE.png',dpi=300)

O = read_outlog('OUTLOG.runmw0br')
plt.plot(O['global']['time'],O[comp]['E'],color='red')
plt.savefig('/Users/mpetersen/Downloads/tE.png',dpi=300)

O = read_outlog('OUTLOG.runmw0br2')
plt.plot(O['global']['time'],O[comp]['E'],color='blue')
plt.savefig('/Users/mpetersen/Downloads/tE.png',dpi=300)
