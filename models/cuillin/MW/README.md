# MW

The directory for Milky Way files.

### Generating ICs

At small scale, this is no real problem. However, as we realise larger and larger phase-spaces, we will need to ask for more resources. For instance, when allocating for 100M/100M particles, we need to request additional memory resources on cuillin, e.g. `srun -N1 -n32 --mem=256G --pty $SHELL`. The ascii files each take 16GB at this point. Each OUT file will take 2.3GB.

### Printing Phase space

We may start to run into phase-space printing bottlenecks. We might want to investigate outputting to fast scratch space and then transferring data.


### Memory footprint

For the `00` series, with 60M total particles, we see (on cuillin)

```
| NVIDIA-SMI 525.89.02    Driver Version: 525.89.02    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA RTX 6000...  Off  | 00000000:31:00.0 Off |                  Off |
| 30%   34C    P2    62W / 300W |   8312MiB / 49140MiB |      0%      Default |
|                               |                      |                  N/A |
```
