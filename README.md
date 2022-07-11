# About `wire-cell-constraint`

## Installation
This is how I created my current setup/enviroment. In the future, if it is useful, I can do something like using a docker image.

### Step 1 - Setup conda enviroment
Create a conda enviroment (or use an existing one if you so choose). To create the enviroment named `wire-cell-constraint-env`, run the command 
```
conda activate wire-cell-constraint-env
```

To activate this enviroment, run 
```
conda activate wire-cell-constraint-env
```

### Step 2 - Install required packages
#### Install pytorch (https://pytorch.org)
**If you want CUDA support**, install the CUDA toolkit version 11.7 and install `pytorch` (with support for cuda) using the following command.

```
conda install pytorch torchvision torchaudio cudatoolkit=11.7 -c pytorch -c conda-forge
```

If you have a different version of cuda installed, you can probably just change the `cudatoolkit=11.7` to something else.


**If you do not have or want CUDA support**, install pytorch using
```
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

#### Install pygeometric (https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html)
To install pygeometric, run
```
conda install pyg -c pyg
```