from collections import deque

def generate_swaps_bfs(source, target):
    def apply_swap(lst, i, j):
        lst = lst[:]  # Copy the list
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    queue = deque([(source, [])])
    seen = set()
    results = set()

    while queue:
        current, swaps = queue.popleft()
        if current == target:
            results.add(tuple(swaps))  # Store unique sequences as tuples
            continue

        seen.add(tuple(current))
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = apply_swap(current, i, j)
                if tuple(swapped) not in seen:
                    queue.append((swapped, swaps + [(i, j)]))

    return list(results)

def generate_swaps_dfs(source, target):
    def apply_swap(lst, i, j):
        lst = lst[:]  # Copy the list
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    def dfs(current, swaps):
        if current == target:
            results.add(tuple(swaps))  # Store unique sequences as tuples
            return
        seen.add(tuple(current))
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = apply_swap(current, i, j)
                if tuple(swapped) not in seen:
                    dfs(swapped, swaps + [(i, j)])

    results = set()  # Use a set to store unique sequences
    seen = set()
    dfs(source, [])
    return list(results)


source = [1, 1, 2, 2]
target = [1, 2, 1, 2]

dfs_sequences = generate_swaps_dfs(source, target)
bfs_sequences = generate_swaps_bfs(source, target)

print("DFS sequences:", len(dfs_sequences))
print("BFS sequences:", len(bfs_sequences))
print("Are they the same?", set(tuple(seq) for seq in dfs_sequences) == set(tuple(seq) for seq in bfs_sequences))

