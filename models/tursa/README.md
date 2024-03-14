# Tursa Accounting

| Date | Hours Remaining | Run Cost |  Nparticles | Nsteps | Notes |
|------------------|---------------|-------------|--------------|----------------|---------------|
| 26-Nov-2023 | 8,763.8 GPUhs | |  60M | 4000 | Test run of MW0 on single GPU node (4 GPUs, `multistep:4,dt:0.002`)|
| 28-Nov-2023 | 8,359.6 GPUhs | 404 | 200M | 4000 | Test run of MW000 on 16 GPUs (`multistep:4,dt:0.002`)|
| 30-Nov-2023 | 7,685.0 GPUhs | 674 | 846M | 1300 | Test run of MW0000 on 32 GPUs (`multistep:3,dt:0.0016`)|
| 03-Dec-2023 | 7,343.7 GPUhs | 341 | 255M | 2600 | Primary solo LMC run, LMC000, on 32 GPUs (`multistep:3,dt:0.0016`) |



## Moving the LMC to the starting location

This will be best accomplished using the `dev` queue to move off the head node but also get going immediately.

## The body files

All particles are 6.e-10 in virial units.

MWhalo: /home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/halo.1670M.bods.diag

MWdisc: /home/dp309/dp309/shared/extreme-mwlmc/models/tursa/MW/MW00000/disc.155M.bods.diag

LMChalo: /home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/halo.250M.bods.diag

LMCdisc: /home/dp309/dp309/shared/extreme-mwlmc/models/tursa/LMC/LMC00/disc.5M.bods.diag

