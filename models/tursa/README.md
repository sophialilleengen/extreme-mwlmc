# Tursa Accounting

| Date | Hours Remaining | Run Cost |  Nparticles | Nsteps | Notes |
|------------------|---------------|-------------|--------------|----------------|---------------|
| 26-Nov-2023 | 8,763.8 GPUhs | |  60M | 4000 | Test run of MW0 on single GPU node (4 GPUs, `multistep:4,dt:0.002`)|
| 28-Nov-2023 | 8,359.6 GPUhs | 404 | 200M | 4000 | Test run of MW000 on 16 GPUs (`multistep:4,dt:0.002`)|
| 30-Nov-2023 | 7,685.0 GPUhs | 674 | 846M | 1300 | Test run of MW0000 on 32 GPUs (`multistep:3,dt:0.0016`)|
| 03-Dec-2023 | 7,343.7 GPUhs | 341 | 255M | 2600 | Primary solo LMC run, LMC000, on 32 GPUs (`multistep:3,dt:0.0016`) |
| 14-Dec-2023 | 4,532.6 GPUhs | 2811 | 1825M | 1400 | Primary solo MW run, MW00000, on 64 GPUs in 47h (`multistep:3,dt:0.0016`)| 
| 18-Dec-2023 | 3,348.7 GPUhs | 1184 | 1825M | 600 | Additional MW steps, on 32 GPUs (two separate 47h runs) |
| 01-Jan-2024 | 6,000.0 GPUhs |      |       |     | reset at first of the year |
| 18-Mar-2024 | 5,127.1 GPUhs | 873  | 2080M | 500 | Full-resolution MW-LMC test (`multistep:3,dt:0.0016`) |  
| 25-Mar-2024 | 2,153.8 GPUhs | 2974 | 2080M | 1500 | Full-resolution MW-LMC production run (`multistep:4,dt:0.0016`)|
| 25-Mar-2024 | 1,880.8 GPUhs | 273  | 2080M | 125 | Increased temporal resolution near peri for full-res MW-LMC |
| 28-Mar-2024 | 1,815.1 GPUhs | 65   | 2080M | 33  | Extra increased temporal resolution near peri for full-res MW-LMC |
| 30-Mar-2024 | project allocation consumed | 1815+ | 2080M | 1500 | Full-resolution MW-LMC with evolved MW | 


At full MWLMC resolution, we have 17 snapshots in the coarse-timestep run (`RunG5`), an additional 7 in the medium-timestep run (`RunG5t`).

## Moving the LMC to the starting location

This will be best accomplished using the `dev` queue to move off the head node but also get going immediately.

`srun -N1 -n1 --qos=dev --partition=gpu-a100-80 --pty --time=1:0:0 $SHELL`

_Actually_ in the end it is faster to do the translation on cuillin and bring back to tursa. To transfer files from cuillin after moving the bodies:
`sleep 60m && scp transformedhalo_RunGrlmc.bods dc-pete4@tursa.dirac.ed.ac.uk:/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MWLMC/ && scp transformeddisc_RunGrlmc.bods dc-pete4@tursa.dirac.ed.ac.uk:/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MWLMC/`

## The body files

All particles are 6.e-10 in virial units.

1. MWhalo: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/halo.1670M.bods.diag`
2. MWdisc: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/disc.155M.bods.diag`
3. LMChalo: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/halo.250M.bods.diag`
4. LMCdisc: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/disc.5M.bods.diag`

To bring the data to a different machine:
`scp "dc-pete4@tursa.dirac.ed.ac.uk:/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MWLMC/outcoef*RunG5*" .`

For an evolved model, we will try to align the later evolution of the solo MW with the infall of the LMC. The last time in the solo MW is T=3.52, so we are targeting T=3.52-1.7=1.82. This means translating an output file to ascii like so: `/home/dp309/dp309/dc-pete4/bin/psp2ascii -f SPL.runmw00000.00011 -a -v`. This makes the new input files 

1. MWhalo: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/comp.mwhalo`
2. MWdisc: `/home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/comp.mwdisc`

with the LMC input files unchanged.



### Getting the cuda compute capability

EXP needs to be compiled with the correct compute capability. If `nvidia-smi` can be run, getting the capability is straightfoward: `nvidia-smi --query-gpu=compute_cap --format=csv`. On tursa, this returns