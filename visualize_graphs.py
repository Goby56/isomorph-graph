import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def read_adjacency_matrix(file_name):
    df = pd.read_csv(file_name, header=None)
    return df.values

def visualize_graph(adj_matrix, graph_title):
    G = nx.from_numpy_array(adj_matrix)
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42) 
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold', edge_color='gray')
    
    plt.title(graph_title)
    plt.show()

G1_adj_matrix = read_adjacency_matrix('graphs/graph2.csv')
G2_adj_matrix = read_adjacency_matrix('graphs/graph3.csv')
visualize_graph(G1_adj_matrix, "Graph 1")
visualize_graph(G2_adj_matrix, "Graph 2")
