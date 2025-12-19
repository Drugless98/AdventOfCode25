import time, math
from pathlib import Path
from functools import wraps

from Model import Machine, Joltage_Requirements, Wiring_Schematics, Light_Diagram

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

class Tree:
    def __init__(self, root: int) -> None:
        self.Root = root
        self.Nodes  = set()
        self.ButtomPressed = 0

    def itterate(self):
        new_combinations = set()
        for node in self.Nodes:
            for second_node in self.Nodes:
                if node == second_node:
                    continue
                else:
                    
            press = node ^ self.Root
            new_combinations.add(press)
        self.Nodes |= new_combinations
        self.ButtomPressed += 1

    def is_valid(self):
        return self.Root in self.Nodes
    


#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read()

    @timeExecution("Task One")
    def TaskOne(self):
        self.Machines = [Machine(i) for i in self.InputData.split("\n")]
        total_button_press = 0

        #: find lowest amount of button press'
        for machine in self.Machines:
            #: make Search tree for machine 
            light_goal = int("".join(["0" if i == "." else "1" for i in machine.Lights]), 2)    
            tree = Tree(light_goal)

            #: add button wiring to the tree
            for wiring in machine.Wiring:
                tree.Nodes.add(int("".join(["1" if i in wiring else "0" for i in range(machine.ButtonsCount)]), 2))

            #: press buttons until path to correct pattern found
            while not tree.is_valid():
                tree.itterate()
            
            #: save buttonpress count
            total_button_press += tree.ButtomPressed
            

    @timeExecution("Task Two")
    def TaskTwo(self):
        pass
        

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")
