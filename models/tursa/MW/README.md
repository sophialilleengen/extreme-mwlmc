## Notes for running on Tursa

There are some idiosyncracies to running on Tursa. In particular, the job submission script requires very specific settings in order to maximise network connectivity.
See here: https://epcced.github.io/dirac-docs/tursa-user-guide/scheduler/#example-job-submission-script-for-grid-parallel-job-using-cuda

This directory has working recipes for Tursa.

### Benchmarks

A run with 100M halo, 100M disc, on 16 GPUs has the following parameters:
```
|===============================+======================+======================|
|   0  NVIDIA A100-SXM...  On   | 00000000:03:00.0 Off |                    0 |
| N/A   29C    P0    66W / 500W |   5276MiB / 81251MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+
```

Reported timings for `multistep:4`
```
----------------------------------------------------------------------
--- Timer info [T=0.002] ---------------------------------------------
----------------------------------------------------------------------
Drift               : 0.121763           [  0.20 %]
Velocity            : 0.251601           [  0.41 %]
Force               : 48.7177            [ 79.87 %]
Coefs               : 1.84684            [  3.03 %]
Output              : 1.9813             [  3.25 %]
Levels              : 0.0329397          [  0.05 %]
Report              : 2.375e-06          [  0.00 %]
Balance             : 1.886e-06          [  0.00 %]
Adjust              : 8.04561            [ 13.19 %]
Cuda copy           : 0.459138           [  0.75 %]
Orient              : 2.01488            [  3.30 %]
Total               : 60.9981            [100.00 %]
----------------------------------------------------------------------
```

`multistep` probably can be reduced to 3, as we currently see
```
------------------------------------------------------------
--- Component <mwhalo, sphereSL>, T=0.002-------------------
------------------------------------------------------------
L  Number    dN/dL     N(<=L)    
------------------------------------------------------------
0  75725017  0.757     0.757     
1  13114757  0.131     0.888     
2  7577842   0.076     0.964     
3  3089235   0.031     0.995     
4  493149    0.005     1.000     
```

### Time Tracking (loose)
| Date | Hours Remaining | Notes |
|------------------|------------------|--------------|
| 26-Nov-2023 | 8,763.8 GPUhs | Test run of MW0 on single GPU |
| XX-Nov-2023 |  GPUhs | Test run of MW000 on 16 GPUs |
