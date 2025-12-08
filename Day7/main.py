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
    def __init__(self, symbol, coords, neighboors):
        self.Symbol: str = symbol
        self.Coords: tuple[int, int] = coords
        self.Neighboors: dict[str, tuple[int, int]] = neighboors
            
class Graph:
    def __init__(self):
        self.Nodes: dict[tuple[int,int], Node] = {}
        self.CurrentNodes: list[Node] | None = None
        self.Splits = 0
        
    def make(self, input_str: str):
        rows = len(input_str)
        cols = len(input_str[0])
        
        for row_idx, row in enumerate(input_str):
            for col_idx, point in enumerate(row):
                if point == "S":
                    self.Root:tuple[int, int] = (row_idx, col_idx)
                    
                self.Nodes[(row_idx, col_idx)] = Node(
                    symbol  = point,
                    coords  = (row_idx, col_idx),
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
    def iterate(self):
        next_nodes = {}
        
        #: On first iteration 
        if self.CurrentNodes is None:
            next_node_coor = self.Nodes.get(self.Root).Neighboors.get("S")
            next_node      = self.Nodes.get(next_node_coor)
            if next_node.Symbol == ".":
                next_node.Symbol = "|"
                self.CurrentNodes = [next_node]
        else:
            for node in self.CurrentNodes:
                #: Get next nodes
                next_node_coor = node.Neighboors.get("S")
                next_node      = self.Nodes.get(next_node_coor)
                
                #: Do we split?
                if next_node is None:
                    return self.Splits
                elif next_node.Symbol == "^":
                    left = self.Nodes.get(next_node.Neighboors.get("W"))
                    right= self.Nodes.get(next_node.Neighboors.get("E"))
                    
                    left.Symbol = "|"
                    right.Symbol= "|"
                    
                    next_nodes[left.Coords] = left
                    next_nodes[right.Coords]= right
                    self.Splits += 1
                else:
                    next_node.Symbol = "|"
                    next_nodes[next_node.Coords] = next_node
                    
            self.CurrentNodes = [next_nodes[i] for i in next_nodes]
        return None
    
    def quantum_iterate(self):
        # Start just below S, same as your classical iterate
        root_node = self.Nodes[self.Root]
        start_coord = root_node.Neighboors.get("S")

        # If S is on the bottom row (weird case), there are no timelines
        if start_coord is None:
            return 0

        # curr: mapping from coordinates -> number of timelines at that cell
        curr: dict[tuple[int, int], int] = {start_coord: 1}
        total_timelines = 0

        while curr:
            new_curr: dict[tuple[int, int], int] = {}

            for coord, count in curr.items():
                node = self.Nodes[coord]

                # Move down from this node
                next_coord = node.Neighboors.get("S")

                # If we can't go further down, all these timelines exit here
                if next_coord is None:
                    total_timelines += count
                    continue

                next_node = self.Nodes[next_coord]

                # If the cell below is a splitter, we branch
                if next_node.Symbol == "^":
                    left_coord = next_node.Neighboors.get("W")
                    right_coord = next_node.Neighboors.get("E")

                    # Each branch gets the FULL count of timelines
                    for branch_coord in (left_coord, right_coord):
                        if branch_coord is None:
                            # This branch immediately exits the manifold
                            total_timelines += count
                        else:
                            new_curr[branch_coord] = new_curr.get(branch_coord, 0) + count

                else:
                    # Normal cell: everything just continues straight down
                    new_curr[next_coord] = new_curr.get(next_coord, 0) + count

            # Move to next "wave" of positions
            curr = new_curr

        return total_timelines
      
#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read().split("\n")

    @timeExecution("Task One")
    def TaskOne(self):
        self.Graph = Graph()
        self.Graph.make(self.InputData)
        
        while True:
            splits = self.Graph.iterate()
            if splits:
                return splits
            
    @timeExecution("Task Two")
    def TaskTwo(self): 
        self.Graph = Graph()
        self.Graph.make(self.InputData)
        
        while True:
            splits = self.Graph.quantum_iterate()
            if splits:
                return splits


if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")