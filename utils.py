from typing import Tuple
import numpy as np
import pandas as pd
import os

GRAPH_DIR = "./graphs"

def generate_isomorphic_graphs(nodes: int) -> Tuple[np.ndarray, np.ndarray]:
    A = np.zeros((nodes, nodes), dtype=int)
    for i in range(nodes):
        for j in range(i + 1, nodes):
            edge = np.random.choice([0, 1])
            A[i, j] = edge
            A[j, i] = edge
    
    permutation = np.random.permutation(nodes)
    
    B = A[np.ix_(permutation, permutation)]
    
    return A, B

def get_graph_filenames():
    return [name for name in os.listdir(GRAPH_DIR) if os.path.isfile(os.path.join(GRAPH_DIR, name))]

def save_graph(ad_matrix, nodes):
    graph_count = len(get_graph_filenames())
    n = len(nodes)
    name = f"graph{graph_count+1}.csv"
    pd.DataFrame(ad_matrix[:n,:n]).to_csv(os.path.join(GRAPH_DIR, name), header=False, index=False)
    print(f"Saved {name} with {n} nodes")

def read_adjacency_matrix(file_name):
    df = pd.read_csv(os.path.join(GRAPH_DIR, file_name), header=None)
    return df.values

def ask_for_int(min_inclusive: int, max_inclusive: int) -> int: 
    options = range(min_inclusive, max_inclusive+1)
    while True:
        inp = input("-> ")
        if inp.isdigit() and int(inp) in options:
            return int(inp)
        else:
            print(f"Please provide an integer ({min_inclusive}-{max_inclusive})")

