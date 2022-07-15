# Wire-Cell Constraint 
## Enviroment Setup
**TODO**: Create Docker/Singularity image

Wire-Cell Constraint relies on PyTorch and PyTorch Geometric, the latter of which is finicky to install. Below details how we were able to install both these packages using `conda` and `spack`. These are of course not the only ways. 

Both these methods were tested on my personal x86-64 Zen2 PC running Ubuntu 22.04. Please tell me what does/does not work for you.
### Using `conda`

This method installs PyTorch 1.11 and PyTorch Geometric 

First, create and activate an enviroment with `python 3.7` installed. Any python higher or lower will cause dependency errors.

Next, to install PyTorch and PyTorch Geometric, run
````
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c conda-forge
conda install pyg -c pyg
````

Make sure both of these were installed correctly by importing them in the python shell.

### Using `pip`
It is also possible to isntall PyTorch and PyTorch Geometric **without cuda support** using pip. Simply run
```
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.12.0+cpu.html
```

### Using `spack`
Installing with `spack` is more difficult then `conda`. Furthermore, it involes a little cheesy hackery in the form of cherry-picking unreleased commits from the `spack` development branch.

#### 1. Cherry Pick Commits
First, cherry pick two commits from this branch:

```
git cherry-pick 52eaedfca28ea6f9fde3a849732c2cdf92e6fefc 5b3e4ba3f8b5ae6cfca5b259211411494d30a336 --allow-empty
```

The first commit adds support for `py-torch 1.12` and the second fixes an issue with a bad checksum for `cuDNN`, a dependency of `py-torch`.

Alternatively, you can simply do a `git checkout develop` and `git pull` to sync with the entire developlement branch. I don't this this a good idea.

Both of these commits will be unecessary once they release `spack` 0.19. The above is only a temporary fix until then.

#### 2. Get correct compilers
Next, make sure you have `gcc-10`, `g++-10`, and `gfortran-10` installed. You can do this through `spack` or `apt`. You need all of these two compile `openmpi`.

Run `spack compiler find` and/or update your [compilers.yaml](https://spack.readthedocs.io/en/latest/getting_started.html#compiler-configuration) manually.

If you did everything correct, your `compilers.yaml` should have something like this:
```
...
- compiler:
    spec: gcc@10.3.0
    paths:
      cc: /usr/bin/gcc-10
      cxx: /usr/bin/g++-10
      f77: /usr/bin/gfortran-10
      fc: /usr/bin/gfortran-10
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
...
```

You may be able to use older/newer versions of `gcc`/`g++`/`gfortran`, but this is what worked for me.

#### 3. Install PyTorch and PyTorch Geometric
Finally, you should be able to install PyTorch and PyTorch geometric with 
```
spack install py-torch-geometric +cuda ^py-torch@1.12.0 cuda_arch=<insert compute capability> %gcc@10.3.0 ^openmpi@4.0
```

You need to replace `<insert compute capability>` with your GPU's [compute capability](https://developer.nvidia.com/cuda-gpus) without the period. For example, I have an RTX 2060 which has compute capability 7.5. Therefore, I will use the variant `cuda_arch=75`.

PyTorch needs to compile with some implementation of `mpi`. By default, it will use `MVAPICH2` which is troublesome to install. It is therefore significantly easier to use `openmpi`.

Finally, if you used a different compiler, change "`gcc@10.3.0`" as needed.

It took around 2.5 to 3 hours to compile everthing on my AMD Ryzen 7 3800x with 32GB of RAM running at 2133 MT/s and an NVME SSD with read and write speeds of 1.0GB/s and 230 MB/s respectively.
