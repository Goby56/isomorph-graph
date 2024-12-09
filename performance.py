import time, random

import numpy as np

from algorithms import IsomorphicChecker
import utils


class PerformanceTest:
    def __init__(self, algorithm: IsomorphicChecker, graph_size: int, iterations: int) -> None:
        self.algorithm = algorithm 
        self.graph_size = graph_size
        self.iterations = iterations
        self.include_non_isomorphic = False
        self.log = True
        self.result = {}

    def start(self):
        total_time = 0
        existing_isomorphisms = 0
        found_isomorphisms = 0

        for _ in range(self.iterations):
            isomorphic = random.random() < 0.3
            A, B = utils.generate_isomorphic_graphs(self.graph_size, isomorphic)
            if isomorphic:
                existing_isomorphisms += 1

            t0 = time.time()
            P = self.algorithm.find_permutation_matrix(A, B)
            dt = (time.time() - t0) * 1000
            if utils.permutation_matrix_check(A, B, P):
                found_isomorphisms += 1
                if self.log:
                    print(f"Found permuations matrix in {dt:.2f}ms")
            else:
                if self.log:
                    print(f"No permutation matrix found ({dt:.2f}ms)")


                
            total_time += dt
        
        self.result["existing_isomorphisms"] = existing_isomorphisms
        self.result["found_isomorphisms"] = found_isomorphisms
        self.result["average_time"] = total_time / self.iterations 

    def __str__(self) -> str:
        return f"Average time: {self.result['average_time']:.2f}ms"
            
