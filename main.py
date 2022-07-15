import os
import torch
import numpy as np
from torch_geometric.data import HeteroData

os.environ['TORCH'] = torch.__version__
print("PyTorch Version", torch.__version__)

# https://github.com/WireCell/wire-cell-toolkit/blob/img-gnn/aux/docs/ClusterArrays.org
# https://github.com/WireCell/wire-cell-python/blob/master/wirecell/img/tap.py#L34

'''
loads all clusters at path into `HeteroData` objects 
one at a time

cnodes, wnodes, snodes, bnodes, mnodes, 
cwedges. bsedges, bwedges, bbedges, cmedges, bmedges
'''
def load_cluster(path):
    with np.load(path) as data:
        n_clusters = len(data.files)//11 # number of clusters in file
        
        # iterate through every cluster
        for i in range(n_clusters):
            get_array = lambda suf: data[f"cluster_{i}_{suf}"]
            
            graph = HeteroData()
            graph["channel"].x = get_array("cnodes").transpose()
            graph["wire"].x = get_array("wnodes").transpose()
            graph["slice"].x = get_array("snodes").transpose() 
            graph["blob"].x = get_array("bnodes").transpose()
            graph["measure"].x = get_array("mnodes").transpose()

            # load edges
            graph["channel", "cw", "wire"].edge_index = get_array("cwedges").transpose()
            graph["blob", "cw", "slice"].edge_index = get_array("bsedges").transpose()
            graph["blob", "cw", "wire"].edge_index = get_array("bwedges").transpose()
            graph["blob", "cw", "blob"].edge_index = get_array("bbedges").transpose()
            graph["channel", "cw", "measure"].edge_index = get_array("cmedges").transpose()
            graph["blob", "cw", "measure"].edge_index = get_array("bmedges").transpose()

            yield graph
            
for graph in load_cluster("./test-cluster-data/clusters-img-5.npz"):
    print(graph)