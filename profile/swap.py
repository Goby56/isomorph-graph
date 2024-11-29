
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


class Swap:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
        self.indices = [i, j]

    def __str__(self) -> str:
        return f"{self.i}, {self.j}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Swap):
            return self.i in other.indices and self.j in other.indices
        return False

    def __hash__(self) -> int:
        return hash((self.i, self.j)) + hash((self.j, self.i))

def generate_permutations(src, dst):
    permuations = set() 
    n = len(src)

    for i in range(n): 
        for j in range(n):
            if src[i] == dst[j]:
                permuations.add(Swap(i+1, j+1))

    return permuations

pA = [3, 2, 1, 1, 2, 3, 1]
pB = [1, 1, 2, 3, 2, 1, 3]

for swap in generate_permutations(pA, pB):
    print(swap)