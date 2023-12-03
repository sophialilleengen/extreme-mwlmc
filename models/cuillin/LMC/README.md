
# LMC models

The models here are the base LMC models, at a variety of particle numbers.

The model with 160M halo, 2.45M disc is half the eventual target. (To even the mass per particle, go to 2.48M disc.)

I've been sequentually turning down the mass of the LMC; different models have different masses.
- 15% Einasto_rs0.035_rhos24.682_alpha0.16_rtrunc33.txt
- 20% Einasto_rs0.035_rhos24.682_alpha0.16_rtrunc32.txt
- 30% Einasto_rs0.035_rhos24.682_alpha0.16_rtrunc31.txt

### Benchmarks

For 160M halo, 2.45M disc (resulting in nearly the same mass per particle), we see
```
|===============================+======================+======================|
|   0  NVIDIA RTX 6000...  Off  | 00000000:31:00.0 Off |                  Off |
| 30%   35C    P2    58W / 300W |  23684MiB / 49140MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```
when looking at the output of `nvidia-smi` on `worker093`. This is well above what could run on `worker001`, so this iteration does not use all 8 GPUs. Rough estimates indicate we could run 140M particles total across the 8 GPUs.

The timing looks like (for `multistep:3`)
```
----------------------------------------------------------------------
--- Timer info [T=0.0016] --------------------------------------------
----------------------------------------------------------------------
Drift               : 0.0238254          [  0.04 %]
Velocity            : 0.0573622          [  0.10 %]
Force               : 40.5396            [ 74.19 %]
Coefs               : 2.21654            [  4.06 %]
Output              : 7.31869            [ 13.39 %]
Levels              : 0.0130807          [  0.02 %]
Report              : 2.223e-06          [  0.00 %]
Balance             : 1.006e-06          [  0.00 %]
Adjust              : 4.47086            [  8.18 %]
Cuda copy           : 2.83552            [  5.19 %]
Orient              : 8.41713            [ 15.40 %]
Total               : 54.64              [100.00 %]
----------------------------------------------------------------------
```
The `Orient` total seems high for `EJ:2`; not sure what is going on there.

with the `multistep` diagnostics
```
------------------------------------------------------------
--- Component <lmchalo, sphereSL>, T=0.0016-----------------
------------------------------------------------------------
L  Number    dN/dL     N(<=L)    
------------------------------------------------------------
0  136789387 0.855     0.855     
1  15338781  0.096     0.951     
2  6540151   0.041     0.992     
3  1331681   0.008     1.000     

T  160000000 

------------------------------------------------------------
--- Component <lmcdisc, cylinder>, T=0.0016-----------------
------------------------------------------------------------
L  Number    dN/dL     N(<=L)    
------------------------------------------------------------
0  2123360   0.867     0.867     
1  284917    0.116     0.983     
2  38806     0.016     0.999     
3  2917      0.001     1.000     
```
