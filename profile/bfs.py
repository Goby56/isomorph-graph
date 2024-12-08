from collections import deque

def generate_swaps_bfs(source, target):
    def apply_swap(lst, i, j):
        lst = lst[:]
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    queue = deque([(source, [])])
    seen = set()
    results = []

    while queue:
        current, swaps = queue.popleft()
        if current == target:
            results.append(swaps)
            continue

        seen.add(tuple(current))
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = apply_swap(current, i, j)
                if tuple(swapped) not in seen:
                    queue.append((swapped, swaps + [(i, j)]))

    return results

source = [1, 1, 2, 2]
target = [1, 2, 1, 2]
swap_sequences = generate_swaps_bfs(source, target)

for seq in swap_sequences:
    print(seq)

print(len(swap_sequences))

