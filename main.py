import inspect
import numpy as np

import utils, algorithms
from algorithms import IsomorphicChecker
from performance import PerformanceTest

def check_isomorphism(A: np.ndarray, B: np.ndarray, algorithm: IsomorphicChecker):
    print(f"Are isomorphic: {algorithm.is_isomorphic(A, B)}")

def test_performance(algorithm: IsomorphicChecker, node_count: int, iterations: int):
    test = PerformanceTest(algorithm, node_count, iterations)
    if input("Generate non isomorphic graphs too? (y/N)").lower() == "y":
        test.all_isomorphic = False
    test.start()
    print(test)

def select_algorithm(ask_for_eigen_check: bool) -> IsomorphicChecker:
    classes = {name: obj for name, obj in inspect.getmembers(algorithms, inspect.isclass)}
    
    print("Which algorithm do you want?")
    subclasses = classes["IsomorphicChecker"].__subclasses__()
    for i, obj in enumerate(subclasses):
        print(f"{i+1}. {obj.__name__}")
    
    choice = utils.ask_for_int(1, len(subclasses))
    SelectedClass = list(subclasses)[choice - 1]

    use_eigen_check = True
    if ask_for_eigen_check: 
        use_eigen_check = input("Use eigen value check? (Y/n)").lower() != "n"
    return SelectedClass(use_eigen_check)

def main():
    print(
    """
    Do you want to check isomorphism between two given graphs 
    or test the performance of an algorithm?
    1. Check isomorphism
    2. Performance test
    """)
    choice = utils.ask_for_int(1, 2)
    if choice == 1:
        print("Select two graphs you want to check.")
        existing_graphs = utils.get_graph_filenames() 
        for g in existing_graphs:
            print(g)
        print("Please select the first graph")
        g1 = utils.ask_for_int(1, len(existing_graphs))
        print("Please select the second graph")
        g2 = utils.ask_for_int(1, len(existing_graphs))
        A = utils.read_adjacency_matrix(f"graph{g1}.csv")
        B = utils.read_adjacency_matrix(f"graph{g2}.csv")
        check_isomorphism(A, B, select_algorithm(True))
    if choice == 2:
        algorithm = select_algorithm(False)
        print("How many nodes should the graphs have?")
        node_count = utils.ask_for_int(2, 50)
        print("For how many iterations should the algorithm run?")
        iterations = utils.ask_for_int(1, 1000)
        test_performance(algorithm, node_count, iterations)


if __name__ == "__main__":
    main()
