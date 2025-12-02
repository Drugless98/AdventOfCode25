import time
import math

from sympy import isprime
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
            self.InputData = file.read().split(",")

    @timeExecution("Task One")
    def TaskOne(self) -> int:
        #: Helper function
        def check_id_valid(id: str) -> bool:
            id_length = len(id)
            middle = int(id_length/2)

            #: Guard statements
            if not id_length % 2 == 0     : return True #: Always valid
            if id[0:middle] == id[middle:]: return False
            return True

        #: Code entry
        self.invalidIds = []
        for sequence in self.InputData:
            sequence_start, sequence_too = sequence.split("-")
            for current_sequence_number in range(int(sequence_start), int(sequence_too)):
                if not check_id_valid(str(current_sequence_number)):
                    self.invalidIds.append(current_sequence_number)
        return sum(self.invalidIds)
    
    @timeExecution("Task Two")
    def TaskTwo(self):
        #: Helper function
        def check_id_valid(id: str) -> bool:
            id_length = len(id)
            middle = int(id_length/2)
            divisors  = [div for div in range(2, middle + 1) if id_length % div == 0]

            #: Guard statements
            if id_length == 1               : return True  #: Length one is always valid
            if all([i == id[0] for i in id]): return False #: if all the same

            for divisor in divisors:                                                #: For every factor / divisor
                chunks = [id[i:i+divisor] for i in range(0, id_length, divisor)]    #: split into smaller arrays
                if all([i == chunks[0] for i in chunks]): return False    #: If all chunks are the same, eg. [1,2], [1,2] return
            return True

        #: Code entry
        self.invalidIds = []
        for sequence in self.InputData:
            sequence_start, sequence_too = sequence.split("-")
            
            for current_sequence_number in range(int(sequence_start), int(sequence_too) + 1):
                if not check_id_valid(str(current_sequence_number)):
                    self.invalidIds.append(current_sequence_number)
        return sum(self.invalidIds)
       


if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")