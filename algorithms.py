from typing import Optional
import numpy as np
from scipy.linalg import eigvals
from itertools import permutations

def equal_eigenvalues(A: np.ndarray, B: np.ndarray) -> bool:
    A_eigenvalues = np.sort(np.round(np.real(eigvals(A)), 4))
    B_eigenvalues = np.sort(np.round(np.real(eigvals(B)), 4))
    return np.array_equal(A_eigenvalues, B_eigenvalues)

class IsomorphicChecker:
    def __init__(self, use_eigen_check: bool) -> None:
        self.use_eigen_check = use_eigen_check

    def is_isomorphic(self, A: np.ndarray, B: np.ndarray) -> bool:
        raise NotImplementedError()

    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        raise NotImplementedError()

class AllPermuations(IsomorphicChecker):
    def is_isomorphic(self, A: np.ndarray, B: np.ndarray) -> bool:
        if self.use_eigen_check and not equal_eigenvalues(A, B):
            return False
        permutation_matrix = self.generate_permuation_matrices(A, B)
        return permutation_matrix != None
    
    def find_permutation_matrix(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        if self.use_eigen_check and not equal_eigenvalues(A, B):
            return None
        return self.generate_permuation_matrices(A, B)

    def generate_permuation_matrices(self, A: np.ndarray, B: np.ndarray) -> Optional[np.ndarray]:
        n = len(A)
        perms = permutations(range(n))
        for perm in perms:
            matrix_P = np.eye(n)[list(perm)]
            if np.array_equal(matrix_P.T @ A @ matrix_P, B):
                return matrix_P
        return None

class FromProfile(IsomorphicChecker):
    def is_isomorphic(self, A: np.ndarray, B: np.ndarray) -> bool:
        source = np.sum(A, axis=0)
        target = np.sum(B, axis=0)
        for seq in self.generate_swaps(source, target):
            pass 
        raise NotImplementedError
    
    def generate_swaps(self, source, target):
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
