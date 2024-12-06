import numpy as np
from itertools import permutations, product

def generate_permutation_matrix(A, B):
    """
    Generate a permutation matrix P such that AP = PA.
    
    Parameters:
    - A: np.ndarray, adjacency matrix of graph 1.
    - B: np.ndarray, adjacency matrix of graph 2.
    
    Returns:
    - A single permutation matrix satisfying the condition, or None if no such matrix exists.
    """
    # Check input validity
    if A.shape != B.shape:
        raise ValueError("Matrices must have the same dimensions.")

    n = A.shape[0]
    
    # Check if row sums match; this is a necessary condition for isomorphism
    row_sums_A = np.sum(A, axis=1)
    row_sums_B = np.sum(B, axis=1)
    if sorted(row_sums_A) != sorted(row_sums_B):
        return None

    # Group rows by their sums
    def group_by_row_sums(matrix):
        row_sum_groups = {}
        for i, row_sum in enumerate(np.sum(matrix, axis=1)):
            if row_sum not in row_sum_groups:
                row_sum_groups[row_sum] = []
            row_sum_groups[row_sum].append(i)
        return row_sum_groups

    groups_A = group_by_row_sums(A)
    groups_B = group_by_row_sums(B)

    # Generate permutations of row indices within matching groups
    matching_permutations = []
    for row_sum in groups_A:
        rows_A = groups_A[row_sum]
        rows_B = groups_B[row_sum]
        if len(rows_A) != len(rows_B):
            return None
        matching_permutations.append(list(permutations(rows_B)))

    # Combine group permutations into overall permutations
    for perm in product(*matching_permutations):
        combined_perm = np.arange(n)
        for group, indices in zip(groups_A.values(), perm):
            for i, index in zip(group, indices):
                combined_perm[i] = index

        # Create the permutation matrix
        P = np.zeros((n, n), dtype=int)
        for i, j in enumerate(combined_perm):
            P[i, j] = 1

        # Check if P satisfies AP = PA
        if np.array_equal(A @ P, P @ B):
            return P  # Return the first valid permutation matrix

    return None  # Return None if no valid permutation matrix is found

def generate_isomorphic_graphs(n):
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            edge = np.random.choice([0, 1])
            A[i, j] = edge
            A[j, i] = edge
    
    permutation = np.random.permutation(n)
    
    B = A[np.ix_(permutation, permutation)]
    
    return A, B

A, B = generate_isomorphic_graphs(18)

permutation_matrices = generate_permutation_matrix(A, B)
print("Permutation Matrices:")
for P in permutation_matrices:
    print(P)
