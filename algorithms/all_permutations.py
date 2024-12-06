import numpy as np
from scipy.linalg import eigvals
from itertools import permutations

def equal_eigenvalues(A, B):
    A_eigenvalues = np.sort(np.round(np.real(eigvals(A)), 4))
    B_eigenvalues = np.sort(np.round(np.real(eigvals(B)), 4))
    return np.array_equal(A_eigenvalues, B_eigenvalues)

def check_permutations(A, B):
    n = len(A)
    perms = permutations(range(n))
    
    for perm in perms:
        matrix_P = np.eye(n)[list(perm)]
        if np.array_equal(matrix_P.T @ A @ matrix_P, B):
            return True, matrix_P

    return False, None

def is_isomorphic(A: np.ndarray, B: np.ndarray):
    if not equal_eigenvalues(A, B):
        return False
    isomorphic, _ = check_permutations(A, B)
    return isomorphic
