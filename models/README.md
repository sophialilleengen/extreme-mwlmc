# Model initial condition construction

## Milky Way

1. Virial radius 122 kpc, virial velocity 149 km/s, virial mass 6.2e11 msun
2. An Einasto halo (with parameters given in `run_makemodel.py`)
3. A disc with a=3.5 kpc (0.029 rvir), b=500 pc (0.004 rvir), total mass of 5.7e10 Msun (0.092 mvir)
4. Realise the disk: `mpirun -np 8 gendisk --config generate_ics.yml`

## Large Magellanic Cloud
