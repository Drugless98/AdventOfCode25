import time
from pathlib import Path
from functools import wraps

#: Time Wrapper
def timeExecution(label: str | None = None):
    """
    Decorator to time function execution.
    Usage:
        @timeExecution()
        def func(): ...

        @timeExecution("Custom name")
        def func(): ...
    """
    def decorator(func):
        name = label or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            print(f"{name} took: {elapsed:.6f}s")
            return result

        return wrapper
    return decorator

class Node:
    def __init__(self, symbol, neighboors):
        self.Symbol: str = symbol
        self.Neighboors: dict[str, tuple[int, int]] = neighboors
            
class Graph:
    def __init__(self):
        self.Nodes: dict[tuple[int,int], Node] = {}
        
    def make(self, input_str: str):
        rows = len(input_str)
        cols = len(input_str[0])
        
        for row_idx, row in enumerate(input_str):
            for col_idx, point in enumerate(row):
                self.Nodes[(row_idx, col_idx)] = Node(
                    symbol  = point,
                    neighboors  = {
                        "N" : (row_idx - 1, col_idx     ) if row_idx > 0                        else None,
                        "NE": (row_idx - 1, col_idx + 1 ) if row_idx > 0 and col_idx < cols - 1 else None,
                        "E" : (row_idx    , col_idx + 1 ) if col_idx < cols - 1                 else None,
                        "SE": (row_idx + 1, col_idx + 1 ) if row_idx < rows - 1 and col_idx < cols - 1 else None,
                        "S" : (row_idx + 1, col_idx     ) if row_idx < rows - 1                 else None,
                        "SW": (row_idx + 1, col_idx - 1 ) if row_idx < rows - 1 and col_idx > 0 else None,
                        "W" : (row_idx    , col_idx - 1 ) if col_idx > 0                        else None,
                        "NW": (row_idx - 1, col_idx - 1 ) if row_idx > 0 and col_idx > 0        else None
                    }
                )
    
    def get_node_symbol(self, coords: tuple[int, int]):
        return self.Nodes[coords].Symbol
    
    def get_neighbor_paper_count(self, coords: tuple[int, int]) -> list[str]:
        node = self.Nodes[coords]
        paperCount = 0
        
        for direction in node.Neighboors:
            coord = node.Neighboors[direction]
            if coord:
                symbol = self.get_node_symbol(coord)
                paperCount += 1 if symbol == "@" else 0 #: Add one if paper else add 0
        return paperCount
    
    def replace_node(self, coord):
        self.Nodes[coord].Symbol = "x"

#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read().split("\n")

    @timeExecution("Task One")
    def TaskOne(self):
        #: make datastructure
        self.graph = Graph()
        self.graph.make(self.InputData)
        paperCount = 0
        
        #: Parse through and count
        for node_coords in self.graph.Nodes:
            if self.graph.get_neighbor_paper_count(node_coords) < 4:
                paperCount += 1 if self.graph.get_node_symbol(node_coords) == "@" else 0
        return paperCount
    
    @timeExecution("Task Two")
    def TaskTwo(self):
        #: Make datastructure
        self.graph = Graph()
        self.graph.make(self.InputData)
        
        #: parse through while anything is returned
        paperCount = 0
        while True:
            iteration_paper_count = 0
            for node_coords in self.graph.Nodes:
                if self.graph.get_neighbor_paper_count(node_coords) < 4:
                    iteration_paper_count += 1 if self.graph.get_node_symbol(node_coords) == "@" else 0
                    self.graph.replace_node(node_coords) #: Make sure to replace @ with x
            
            if iteration_paper_count > 0:
                paperCount += iteration_paper_count
            else:
                break
        return paperCount

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")