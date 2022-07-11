import os
import numpy as np
import torch

os.environ['TORCH'] = torch.__version__
print("PyTorch Version", torch.__version__)