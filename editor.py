import pygame, sys, math, os
import numpy as np
import pandas as pd

DIM = (1200, 600) # dimensions
GRAPH_DIR = "./graphs"
NODE_SIZE = 30
MAX_NODES = 50
EDGE_THICKNESS = 3

ad_matrix = np.zeros((MAX_NODES, MAX_NODES), dtype=np.int8)

nodes = []

selected_node = -1

def get_graph_filenames():
    return [name for name in os.listdir(GRAPH_DIR) if os.path.isfile(os.path.join(GRAPH_DIR, name))]

def handle_click(mouse_pos, selected_node, ad_matrix):
    x, y = mouse_pos
    i = node_collision(x, y)
    if i == -1:
        nodes.append((x, y))
        return selected_node
    
    if selected_node == -1:
        return i

    create_connection(selected_node, i, ad_matrix)
    return -1 
    
def node_collision(x, y):
    for i, node in enumerate(nodes):
        dx, dy = node[0] - x, node[1] - y
        if math.sqrt(dx*dx + dy*dy) < NODE_SIZE:
            return i
    return -1

def create_connection(i, j, ad_matrix):
    ad_matrix[i, j] = 1
    ad_matrix[j, i] = 1

def save_graph(ad_matrix):
    graph_count = len(get_graph_filenames())
    n = len(nodes)
    name = f"graph{graph_count+1}.csv"
    pd.DataFrame(ad_matrix[:n,:n]).to_csv(os.path.join(GRAPH_DIR, name), header=False, index=False)
    print(f"Saved {name} with {n} nodes")

def read_adjacency_matrix(file_path):
    df = pd.read_csv(file_path, header=None)
    return df.values

# if input("Read from existing graph? (y/N)") == "y":
#     existing_graphs = get_graph_filenames() 
#     for g in existing_graphs:
#         print(g)
#     n = int(input(f"Please select a graph (1-{len(existing_graphs)})"))
#     m = read_adjacency_matrix(os.path.join(GRAPH_DIR, f"graph{n}.csv"))
#     ad_matrix[:m.shape[0],:m.shape[1]] = m

pygame.init()
window = pygame.display.set_mode(DIM)
window.fill((25, 25, 25))
pygame.display.set_caption("Graph editor")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                save_graph(ad_matrix)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_node = handle_click(pygame.mouse.get_pos(), selected_node, ad_matrix)

    window.fill((25, 25, 25))

    for g in range(MAX_NODES):
        for j in range(MAX_NODES):
            if ad_matrix[g, j]:
                pygame.draw.line(window, (128, 128, 128), nodes[g], nodes[j], EDGE_THICKNESS)

    for g, node in enumerate(nodes):
        if g == selected_node:
            pygame.draw.circle(window, (255, 255, 255), node, NODE_SIZE + 3)
        pygame.draw.circle(window, (128, 128, 128), node, NODE_SIZE)
    

    pygame.display.update()

    clock.tick(20)
