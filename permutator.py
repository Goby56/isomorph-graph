import numpy as np

def equal_profile(pA, pB):
    edgesA = {}
    edgesB = {}
    for i in range(len(pA)):
        if pA[i] in edgesA:
            edgesA[pA[i]] += 1
        else:
            edgesA[pA[i]] = 1

        if pB[i] in edgesB:
            edgesB[pB[i]] += 1
        else:
            edgesB[pB[i]] = 1
    
    for key in edgesA.keys():
        if key not in edgesB:
            return False
        if edgesA[key] != edgesB[key]:
            return False
    return True

def generate_permutation_matrix(src, dst):
    n = len(src)
    P = np.eye(n)

    for i in range(n): 
        swap = i
        if src[i] != dst[i]:
            swap = find_swap(src, dst, i)
            if not swap: return False, None
            temp = src[i]
            src[i] = src[swap]
            src[swap] = temp

        E = np.eye(n)
        E[[i, swap]] = E[[swap, i]]
        P = E @ P
    return True, P

def find_swap(src, dst, start):
    target = dst[start]
    for i in range(start+1, len(src)):
        if src[i] == target:
            return i
    return False
