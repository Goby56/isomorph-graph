def generate_swaps_iterative(source, target):
    def apply_swap(lst, i, j):
        lst = lst[:]
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    stack = [(source, [])]
    seen = set()
    results = set()  # Use a set to store unique sequences of swaps

    while stack:
        current, swaps = stack.pop()
        if current == target:
            results.add(tuple(swaps))  # Store the sequence of swaps as a tuple
            continue

        seen.add(tuple(current))

        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                swapped = apply_swap(current, i, j)
                if tuple(swapped) not in seen:
                    stack.append((swapped, swaps + [(i, j)]))

    return [list(seq) for seq in results]  # Convert back to list format


source = [1, 1, 2, 2, 3, 3, 4, 4]
target = [1, 2, 3, 4, 1, 2, 3, 4]
swap_sequences = generate_swaps_iterative(source, target)

for seq in swap_sequences:
    print(seq)

print(len(swap_sequences))
