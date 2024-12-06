import numpy as np

def generate_swaps(source, target):
    # Helper function to apply a swap to a list
    def apply_swap(lst, i, j):
        lst = lst[:]  # Make a copy to avoid modifying the original
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    # Recursive function to explore all swaps
    def dfs(current, swaps):
        if current == target:
            results.append(swaps)

            return
        seen.add(tuple(current))
        # Try all possible swaps
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = apply_swap(current, i, j)
                if tuple(swapped) not in seen:
                    dfs(swapped, swaps + [(i, j)])
    
    results = []
    seen = set()
    dfs(source, [])
    return results

def is_isomorphic(A: np.ndarray, B: np.ndarray):
    for seq in generate_swaps(np.sum(A, axis=0), np.sum(B, axis=0)):
        pass 

