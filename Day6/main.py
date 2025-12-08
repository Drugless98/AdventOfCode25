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


#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read().split("\n")

    @timeExecution("Task One")
    def TaskOne(self):
        import re, math
        problems: dict[int, list] = {}
        
        #: Parse input and save it in above problems dict
        for row in self.InputData:
            col_numbers = re.findall("(\d+|[+\-*/])", row)
            
            for idx, col in enumerate(col_numbers):
                if idx in problems:
                    problems[idx].append(col)
                else: 
                    problems[idx] = [int(col)]
        
        #: Calculate the parsed input
        problem_solutions = []
        for i in problems:
            problem: list = problems[i][:-1]
            func          = problems[i][-1]
            
            if func == "+":
                problem_solutions.append(sum([int(i) for i in problem]))
            elif func == "*":
                problem_solutions.append(math.prod([int(i) for i in problem]))
        return sum(problem_solutions)
            
    @timeExecution("Task Two")
    def TaskTwo(self): 
        import math  
        problems: dict[int, list] = {}
        
        #: Parse inputs per char
        for row in self.InputData[:-1]:
            for idx, col in enumerate(reversed(row)):
                if idx in problems:
                    problems[idx] += col
                else:
                    problems[idx] = col
        symbols = [i for i in reversed(self.InputData[-1]) if not i == " "]
                    
        #: further parse problems
        counter = 0
        parsed_problems: list[list[str]] = []
        
        for i in problems:
            if len(parsed_problems) == counter:
                parsed_problems.append([])
            
            value:str = problems[i]
            if not value == "    ":
                parsed_problems[counter].append(value.strip())
            else:
                parsed_problems[counter].append(symbols[counter])
                counter += 1
        parsed_problems[counter].append(symbols[counter])
        
        #: Calculate the parsed input
        problem_solutions = []
        for idx, problem in enumerate(parsed_problems):
            problem: list = parsed_problems[idx][:-1]
            func          = parsed_problems[idx][-1]
            
            if func == "+":
                problem_solutions.append(sum([int(i) for i in problem]))
            elif func == "*":
                problem_solutions.append(math.prod([int(i) for i in problem]))
        return sum(problem_solutions)


if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")