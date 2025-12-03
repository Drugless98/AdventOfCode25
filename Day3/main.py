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
    #: Helper
        def find_largest(arr):
            """Return the largest (not last) number in an array and its index as tuple (number, idx)"""
            largest_found = (-1, -1) #: (number, idx)
            
            #: Go through arr and return largest, not last, number and index
            for idx, i in enumerate(arr[:-1]): 
                i = int(i)
                if i > largest_found[0]:
                    largest_found = (i, idx)
            return largest_found

    #: Code Entry
        jolt_sum = 0
        for bank in self.InputData:
            largest, idx = find_largest(bank)
            second_largest = max(bank[idx+1:])
            jolt_sum += int(f"{largest}{second_largest}")
        return jolt_sum
    
    @timeExecution("Task Two")
    def TaskTwo(self):
        #: Helper
        def find_largest(arr, limit):
            """
                Return the largest number, within given limit (limit is number of digits to be kept on the right)
                in an array and its index as tuple (number, idx)
            """
            largest_found = (-1, -1) #: (number, idx)
            
            #: Go through arr and return largest, within limit
            itter_arr = arr[:-limit] if limit > 0 else arr
            for idx, i in enumerate(itter_arr): 
                i = int(i)
                if i > largest_found[0]:
                    largest_found = (i, idx)
            return largest_found

        #: Code Entry
        jolt_sum = 0
        for bank in self.InputData:

            stepper = 0 #: We need 12 digits so keep 12 digits on the right first time picking largest, then 11, 10 ect.
            bank_jolts = ""
            for i in range(11, -1, -1): #: we pick 12 so we start with a limit of 11
                largest, idx = find_largest(bank[stepper:], i)
                stepper = idx + 1 + stepper
                bank_jolts = f"{bank_jolts}{largest}"
            jolt_sum += int(bank_jolts)
        return jolt_sum

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")