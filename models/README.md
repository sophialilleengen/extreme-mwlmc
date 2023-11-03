# Model initial condition construction

## Milky Way

1. Virial radius 122 kpc, virial velocity 149 km/s, virial mass 6.2e11 msun
2. An Einasto halo (with parameters given in `MW/run_makemodel_mw.py`), halo cutoff[^1] is at 20 rscale
3. A disc with a=3.5 kpc (0.029 rvir), b=500 pc (0.004 rvir), total mass of 5.7e10 Msun (0.092 mvir)
4. Realise the disk: `mpirun -np 8 gendisk --config generate_ics.yml`


## Large Magellanic Cloud

1. Using the virial parameters from the Milky Way
2. Einasto halo (with parameters given in `LMC/run_makemodel_lmc.py`), halo cutoff at 30 rscale
3. A disc with a=1.7 kpc (0.014 rvir), b=340 pc (0.003 rvir), total mass of 3.1e9 Msun (0.005 mvir)
4. Realise the disk: `mpirun -np 8 gendisk --config LMC/generate_ics_lmc.yml`


[^1]: The halo cutoff is the smallest possible at which the density (2nd value in the final line of the output of `run_makemodel.py`) is not zero but very small.
