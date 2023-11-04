# MW

The directory for Milky Way files.

### Generating ICs

At small scale, this is no real problem. However, as we realise larger and larger phase-spaces, we will need to ask for more resources. For instance, when allocating for 100M/100M particles, we need to request additional memory resources on cuillin, e.g. `srun -N1 -n36 --mem=64G --pty $SHELL`. The ascii files each take 16GB at this point. Each OUT file will take 2.3GB.
