from typing import Optional
import numpy as np
from scipy.linalg import eigvals
from itertools import permutations, product

import utils

def equal_eigenvalues(A: np.ndarray, B: np.ndarray) -> bool:
    A_eigenvalues = np.sort(np.round(np.real(eigvals(A)), 4))
    B_eigenvalues = np.sort(np.round(np.real(eigvals(B)), 4))
    return np.array_equal(A_eigenvalues, B_eigenvalues)

class IsomorphicChecker:
    def __init__(self, use_eigen_check: bool) -> None:
        self.use_eigen_check = use_eigen_check

    def is_isomorphic(self, A: np.ndarray, B: np.ndarray) -> bool:
        if self.use_eigen_check and not equal_eigenvalues(A, B):
            print("Non equal eigenvalues")
            return False
        permutation_matrix = self.find_permutation_matrix(A, B)
        return isinstance(permutation_matrix, np.ndarray)

    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        raise NotImplementedError()

class AllPermuations(IsomorphicChecker):
    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        n = len(A)
        perms = permutations(range(n))
        for perm in perms:
            matrix_P = np.eye(n)[list(perm)]
            if utils.permutation_matrix_check(A, B, matrix_P):
                return matrix_P
        return None

class DepthFirstSearch(IsomorphicChecker):
    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        source = np.sum(A, axis=0)
        target = np.sum(B, axis=0)
        
        # If the two matrices don't have the same 
        # degrees no permutation matrix can exist
        if not np.array_equal(np.sort(source), np.sort(target)):
            return None
        
        # Create a new list with i and j swapped
        def swap(lst, i, j):
            lst = lst[:]
            lst[i], lst[j] = lst[j], lst[i]
            return lst

        seen = set()
        # Recursive function to explore all swaps
        def dfs(current, swaps):
            if np.array_equal(current, swaps):
                P = utils.get_permutation_matrix_from_swaps(len(A), swaps)
                if np.array_equal(P.T @ A @ P, B):
                    return P

            seen.add(tuple(current))
            # Try all possible swaps
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    swapped = swap(current, i, j)
                    if tuple(swapped) not in seen:
                        return dfs(swapped, swaps + [(i, j)])
        
        return dfs(source, [])

class DegreeGrouping(IsomorphicChecker):
    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        source = np.sum(A, axis=0)
        target = np.sum(B, axis=0)
        n = len(A)
        
        # If the two matrices don't have the same 
        # degrees no permutation matrix can exist
        if not np.array_equal(np.sort(source), np.sort(target)):
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

            if np.array_equal(A @ P, P @ B):
                return P

        return None
