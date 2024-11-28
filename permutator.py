import re
from typing import List, Self, Tuple
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

class SwapTree:
    def __init__(self) -> None:
       self.children = [] 

class Profile:
    permutations = []

    def __init__(self, degrees, blacklist: List | None = None, swap: Tuple[int, int] | None = None) -> None:
        self.degrees = degrees
        print(self.degrees)
        self.swaps = []
        if swap != None:
            self.swaps.append(swap)

        if blacklist != None:
            self.blacklist = blacklist
        else:
            self.blacklist = [0 for _ in range(len(self.degrees))]

    def swap(self, i, j):
        new_degrees = self.degrees[::]
        new_blacklist = self.blacklist[::]

        temp = new_degrees[i]
        new_degrees[i] = new_degrees[j]
        new_degrees[j] = temp
        new_blacklist[j] = 1
        return Profile(new_degrees, new_blacklist, (i, j))

    def find_permutations(self, goal: Self):
        n = len(self.degrees)
        if self == goal: 
            Profile.permutations.append(self.swaps)
            return

        for i in range(n):
            for j in range(n):
                if i == j: continue
                if self.blacklist[i] or self.blacklist[j]:
                    continue
                if self.degrees[i] == goal.degrees[j]:
                    new_profile = self.swap(i, j)
                    new_profile.find_permutations(goal)


    def __eq__(self, other) -> bool:
        if isinstance(other, Profile):
            if len(self.degrees) != len(other.degrees):
                return False
            for i in range(len(self.degrees)):
                if self.degrees[i] != other.degrees[i]:
                    return False
            return True
        return False
                    
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

# for swap in generate_permutations(pA, pB):
#     print(swap)

profile = Profile(pA)

profile.find_permutations(Profile(pB))

for perm in Profile.permutations:
    print(perm)
