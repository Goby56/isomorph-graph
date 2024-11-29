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

def V1(A, B):
    if not equal_eigenvalues(A, B):
        return False
    isomorphic, matrix_P = check_permutations(A, B)
    print(matrix_P)
    return isomorphic


def main():
    A, B = generate_isomorphic_graphs(5)
    print(A)
    print(B)

if __name__ == "__main__":
    main()
