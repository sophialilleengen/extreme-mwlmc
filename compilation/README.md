# Compilation hints on Cosma and Tursa

## Cosma

Cosma-8 is the primary CPU machine we will use for the mSSA runs. This is a mature machine that is bordering on module morass, but EXP pieces appear to be mostly working. The correct module set includes a custom-built HDF5 module: `module load cosma/2018 cmake/3.25.1 gnu_comp/13.1.0 openmpi/4.1.4  modhdf5/1.14.0 fftw/3.3.9 python/3.10.12`

The compilation is located in `/cosma/home/dp309/dc-pete4/EXP`. Assuming all sets done as below...
```
export INCLUDE=/cosma/local/parallel_hdf5/gnu_13.1.0_ompi_4.1.4/1.14.0/include/:$INCLUDE

cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_CUDA=NO -DENABLE_USER=ON -DENABLE_PYEXP=YES -DHDF5_INCLUDE_DIRS=/cosma/local/parallel_hdf5/gnu_13.1.0_ompi_4.1.4/1.14.0/include/ -DCMAKE_INSTALL_PREFIX=/cosma/home/dp309/dc-pete4/ -DPYTHON_EXECUTABLE=$(python3 -c "import sys; print(sys.executable)") -Wno-dev ..

make -j 32
make install
```

Note that to use `pyEXP`, you will need `python3`, as the default `python` on the system fails. To point at my version of `pyEXP`, all one needs to do is use python's `os` library, e.g.

```
import os
pwd = os.getcwd()
os.chdir('/cosma/home/dp309/dc-pete4/EXP/build/pyEXP')
import pyEXP
os.chdir(pwd)
```

### Setup steps needed on Cosma

#### HDF5

I had to modify the HDF5 module, using the file `/cosma/local/Modules/modulefiles/libraries/hdf5/1.14.0` as the base, simply removing the line `AddF90ModuleDir $pkgroot/include/shared/`, which is not needed.
```
# https://researchcomputing.princeton.edu/support/knowledge-base/custom-modules
mkdir /cosma/home/dp309/dc-pete4/Modules/modulefiles/modhdf5
nano 1.14.0
# edit the HDF5 module version
```

#### eigen
I had to install eigen.
```
# we need eigen? This is version 3.4.90
git clone https://gitlab.com/libeigen/eigen.git
cd eigen
mkdir build
cmake ..
cmake . -DCMAKE_INSTALL_PREFIX=/cosma/home/dp309/dc-pete4/
make install
```

I wrote some simple verification codes. First, `version.cpp`:
```
#include <iostream>
#include <Eigen/Core>

int main() {
    std::cout << "Eigen Version: "
              << EIGEN_WORLD_VERSION << "."
              << EIGEN_MAJOR_VERSION << "."
              << EIGEN_MINOR_VERSION << std::endl;
    return 0;
}
```

And a minimal diagnostic code to try and understand a Tensor issue:
```
#include <iostream>
#include <Eigen/Core>
#include <Eigen/CXX11/Tensor>

int main() {
    Eigen::Tensor<double, 3> tensor;

    int rows = 10;
    int cols = 6;
    int depth = 3;

    // Attempt to resize the tensor ambiguously
    tensor.resize({rows, cols, depth});

/*
    // Resize the tensor using explicit type information
    tensor.resize(Eigen::array<Eigen::Index, 3>{rows, cols, depth});
*/

    std::cout << "Resized tensor dimensions: " << tensor.dimensions() << std::endl;

    return 0;
}
```

These were built and tested like so:
```
# make some test scripts work.
# if you compile these in the eigen folder, all hell breaks loose. So, don't.
g++ -I../eigen version.cpp -o version
./version
g++ -I../eigen -Iunsupported failure.cpp -o failure
```

## Tursa

Tursa is the primary GPU machine that we will use for the n-body runs. The machine is still under development, so there are some challenges (see below). The base modules are loaded with `module load gcc/9.3.0 cuda/11.4.1  openmpi/4.1.1-cuda11.4.1`.

The compilation is located in `/home/dp309/dp309/dc-pete4/EXP/`. Assuming all setps below have been completed, one can simply:
```
cmake -DCMAKE_C_COMPILER=/mnt/lustre/tursafs1/apps/gcc/9.3.0/bin/gcc  -DCMAKE_BUILD_TYPE=Release -DENABLE_CUDA=YES -DENABLE_USER=ON -DENABLE_PYEXP=NO -DCMAKE_INSTALL_PREFIX=/home/dp309/dp309/dc-pete4/ -Wno-dev ..

make -j 32
make install
```


### Compiling additional libraries on Tursa

Tursa does not have much by default. In fact, `cmake` is an additional module that must be loaded separately!

```
module use /home/y07/shared/tursa-modules
module load cmake
```

One must also remember to load the external submodules from the start:
```
cd EXP
git submodule update --init --recursive

mkdir build
```

#### FFTW3

FFTW3 is not a necessary part of the software, but we might want it. There is no github that I can find, so proceed the old-fashioned way of downloading the tarball and moving to Tursa. Then,
```
# tar -xvf fftw-3.3.10.tar
cd /home/dp309/dp309/dc-pete4/fftw-3.3.10
./configure --prefix=/home/dp309/dp309/dc-pete4/ CFLAGS="-fPIC" CXXFLAGS="-fPIC"
make -j 32
make install
```

#### Eigen

Eigen is header-only, but compiling in theory makes it easier for `cmake` to find the correct paths.

```
git clone https://gitlab.com/libeigen/eigen.git
cd eigen
mkdir build
cd build
cmake -DCMAKE_C_COMPILER=/mnt/lustre/tursafs1/apps/gcc/9.3.0/bin/gcc -DCMAKE_INSTALL_PREFIX=/home/dp309/dp309/dc-pete4/ ..
make install
```

Then, to `CMakeLists.txt`, add `include_directories(/home/dp309/dp309/dc-pete4/include/eigen3)` to be absolutely sure of picking up the right path.

#### HDF5


```
git clone git@github.com:HDFGroup/hdf5.git
cd hdf5
git checkout remotes/origin/hdf5_1_14_2
mkdir build
cd build

# if the module set changes, this will probably also need to change.
cmake -DCMAKE_C_COMPILER=/mnt/lustre/tursafs1/apps/gcc/9.3.0/bin/gcc -DCMAKE_BUILD_TYPE:STRING=Release -DBUILD_SHARED_LIBS:BOOL=OFF -DHDF5_BUILD_CPP_LIB=ON -DCMAKE_INSTALL_PREFIX=/home/dp309/dp309/dc-pete4/ ..

make -j 32
make install
```

There is one more trick to make HDF5 and HighFive work, owing to what appear to be some compiler bugs. Follow these instructions:
```
https://github.com/keichi/HighFive/commit/0f63bd88086ba761531a0d00228ba8118563d8fa
# extern/HighFive/include/highfive/H5Selection.hpp
# and remove the friend class lines in H5Group.hpp
# extern/HighFive/include/highfive/H5Group.hpp
```
