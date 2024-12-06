
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

source = [3, 2, 1, 1, 2, 3, 1]
target = [1, 1, 2, 3, 2, 1, 3]
swap_sequences = generate_swaps(source, target)


for seq in swap_sequences:
    print(seq)

print(len(swap_sequences))
