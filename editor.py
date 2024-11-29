import pygame, sys, math, os, random
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

def handle_click(mouse_button, mouse_pos, selected_node, ad_matrix):
    right_click = mouse_button == 3 
    x, y = mouse_pos
    collided_node = node_collision(x, y)
    if collided_node != -1:
        if right_click:
            remove_node(collided_node)
            return -1
        if selected_node == -1:
            return collided_node
        create_connection(selected_node, collided_node, ad_matrix)
        
    if collided_node == -1 and not right_click:
        nodes.append([x, y])
        return selected_node

    return -1 
    
def node_collision(x, y):
    for i, node in enumerate(nodes):
        dx, dy = node[0] - x, node[1] - y
        if math.sqrt(dx*dx + dy*dy) < NODE_SIZE:
            return i
    return -1

def create_connection(i, j, ad_matrix):
    ad_matrix[i, j] = not ad_matrix[i, j]
    ad_matrix[j, i] = not ad_matrix[j, i]

def remove_node(i):
    ad_matrix[:i, i:-1] = ad_matrix[:i, i+1:]  # Shift top-right to the left
    ad_matrix[i:-1, :i] = ad_matrix[i+1:, :i]  # Shift bottom-left upwards
    ad_matrix[i:-1, i:-1] = ad_matrix[i+1:, i+1:]  # Shift bottom-right to top-left

    # Fill the last row and column with zeros
    ad_matrix[-1, :] = 0  # Last row
    ad_matrix[:, -1] = 0  # Last column
    nodes.pop(i)

def save_graph(ad_matrix):
    graph_count = len(get_graph_filenames())
    n = len(nodes)
    name = f"graph{graph_count+1}.csv"
    pd.DataFrame(ad_matrix[:n,:n]).to_csv(os.path.join(GRAPH_DIR, name), header=False, index=False)
    print(f"Saved {name} with {n} nodes")

def read_adjacency_matrix(file_path):
    df = pd.read_csv(file_path, header=None)
    return df.values

if input("Read from existing graph? (y/N)") == "y":
    existing_graphs = get_graph_filenames() 
    for g in existing_graphs:
        print(g)
    n = int(input(f"Please select a graph (1-{len(existing_graphs)})"))
    m = read_adjacency_matrix(os.path.join(GRAPH_DIR, f"graph{n}.csv"))
    ad_matrix[:m.shape[0],:m.shape[1]] = m
    for i in range(m.shape[0]):
        random.seed(i)
        x = random.uniform(0, DIM[0])
        y = random.uniform(0, DIM[1])
        nodes.append([x, y])

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
            selected_node = handle_click(event.button, pygame.mouse.get_pos(), selected_node, ad_matrix)

    window.fill((25, 25, 25))

    for i in range(MAX_NODES):
        for j in range(MAX_NODES):
            if ad_matrix[i, j]:
                pygame.draw.line(window, (128, 128, 128), nodes[i], nodes[j], EDGE_THICKNESS)
    
    degrees = np.sum(ad_matrix, axis=0)
    c = 2 / max(1, max(degrees))
    for i, node in enumerate(nodes):
        redness = int(255 / (1 + math.exp(-c * degrees[i])))
        if i == selected_node:
            pygame.draw.circle(window, (255, 255, 255), node, NODE_SIZE + 3)
        pygame.draw.circle(window, (redness, 255 - redness, 255 - redness), node, NODE_SIZE)
    
    pygame.display.update()

    clock.tick(20)
