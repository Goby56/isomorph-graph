import time as timer

from algorithms import IsomorphicChecker
import utils


class PerformanceTest:
    def __init__(self, algorithm: IsomorphicChecker, graph_size: int, iterations: int) -> None:
        self.algorithm = algorithm 
        self.graph_size = graph_size
        self.iterations = iterations
        self.log = True
        self.result = {}

    def start(self):
        total_time = 0

        for _ in range(self.iterations):
            A, B = utils.generate_isomorphic_graphs(self.graph_size)
            t0 = timer.time()
            self.algorithm.find_permutation_matrix(A, B)
            dt = (timer.time() - t0) * 1000
            if self.log:
                print(f"Found permuations matrix in {dt:.2f}ms")
            total_time += dt

        self.result["average_time"] = total_time / self.iterations 

    def __str__(self) -> str:
        return f"Average time: {self.result['average_time']:.2f}ms"
            
