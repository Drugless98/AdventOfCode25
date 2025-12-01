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

#: Class' for linked lists
class Node:
    def __init__(self) -> None:
        self.Left  = None
        self.Right = None
        self.Visited = 0

class LinkedList:
    def __init__(self) -> None:
        self.Root = None
        self.ZeroNode = None

    def make(self, size, root):
        self.Nodes = [Node() for _ in range(size)]

        #: Set all nodes
        for i, node in enumerate(self.Nodes):
            node.Left = self.Nodes[i-1] if i > 0 else self.Nodes[size-1]
            node.Right= self.Nodes[i+1] if i < 99 else self.Nodes[0]

        #: Set root
        self.Root = self.Nodes[root]
        self.ZeroNode = self.Nodes[0]
        return self.Root

#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read().split("\n")

    @timeExecution("Task One")
    def TaskOne(self):
         #: Make linked list
        self.LinkedList = LinkedList()
        selected_node:Node = self.LinkedList.make(100, 50)

        #: Go through each instruction 
        for instruction in self.InputData:
            
            #: Read instruction 
            direction   = instruction[0]
            steps       = int(instruction[1:])

            #: go through list until new dialPoint hit
            for _ in range(steps):
                if direction == "L":
                    selected_node = selected_node.Left
                else:
                    selected_node = selected_node.Right

            if selected_node == self.LinkedList.ZeroNode:
                selected_node.Visited += 1     
        return self.LinkedList.ZeroNode.Visited
    
    @timeExecution("Task Two")
    def TaskTwo(self):
        #: Make linked list
        self.LinkedList = LinkedList()
        selected_node:Node = self.LinkedList.make(100, 50)

        #: Go through each instruction 
        for instruction in self.InputData:
            
            #: Read instruction 
            direction   = instruction[0]
            steps       = int(instruction[1:])

            #: go through list until new dialPoint hit
            for step in range(steps):
                if direction == "L":
                    selected_node = selected_node.Left
                else:
                    selected_node = selected_node.Right

                if selected_node == self.LinkedList.ZeroNode:
                    selected_node.Visited += 1     
        return self.LinkedList.ZeroNode.Visited


if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")