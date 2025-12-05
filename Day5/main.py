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
    def __init__(self, lower_bound, upper_bound) -> None:
        self.Left:  Node | None = None
        self.Right: Node | None = None
        self.Lower_bound: int = lower_bound
        self.Upper_bound: int = upper_bound

class BST:
    def __init__(self, root) -> None:
        self.Root = root

    def _reinsert_subtree(self, node: Node, subtree: Node | None) -> Node:
        if subtree is None:
            return node
        node = self.insert(node, (subtree.Lower_bound, subtree.Upper_bound))
        node = self._reinsert_subtree(node, subtree.Left)
        node = self._reinsert_subtree(node, subtree.Right)
        return node
    
    def insert(self, node: Node | None, key: tuple[int, int]) -> Node | None:    
        low, high = key

        if self.Root is None:
            self.Root = Node(low, high)
            return self.Root

        if node is None:
            return Node(low, high)

        
        if (node.Lower_bound, node.Upper_bound) == key:
            return node
        
        if node.Lower_bound <= low and low <= node.Upper_bound and high > node.Upper_bound: #: If key_low overlap
            node.Upper_bound = high
            #: recheck if any nodes on the right can now fit in this range
            if node.Right:
                right = node.Right
                node.Right = None
                node = self._reinsert_subtree(node, right)
            return node
        
        elif node.Lower_bound <= high and high <= node.Upper_bound and low < node.Lower_bound: #: if key_high overlap
            node.Lower_bound = low
            #: recheck if any nodes on the right can now fit in this range
            if node.Left:
                left = node.Left
                node.Left = None
                node = self._reinsert_subtree(node, left)
            return node
        
        elif node.Lower_bound <= low and high <= node.Upper_bound: #: if both overlap and is smaller
            return node
        
        elif node.Lower_bound >= low and high >= node.Upper_bound: #: if both overlap and is bigger
            node.Lower_bound = low
            node.Upper_bound = high
            return node

        elif node.Lower_bound > low:
            node.Left = self.insert(node.Left, key) #: if no overlap
        else:
            node.Right= self.insert(node.Right, key)
        return node
    
    def id_in_range(self, node: Node  | None, id: int) -> bool:
        """Search through the BST for a range that contain the id"""
        if node is None:
            return False
        
        if node.Lower_bound <= id and node.Upper_bound >= id:
            return True
        else:
            return self.id_in_range(node.Left, id) or self.id_in_range(node.Right, id)
        
    def get_tree_range(self, node: Node | None) -> int:
        if node is None:
            return 0
        else:
            return  (node.Upper_bound - node.Lower_bound + 1) + self.get_tree_range(node.Left) + self.get_tree_range(node.Right)

#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read()

    @timeExecution("Task One")
    def TaskOne(self):
        self.BST  = BST(None)
        self.Root = self.BST.Root

        #: Parse input
        database, ingredients = self.InputData.split("\n\n")
        database    = database.split("\n")
        ingredients = ingredients.split("\n")
        
        #: Make BST
        for data in database:
            low, high = data.split("-") 
            self.Root = self.BST.insert(self.Root, (int(low), int(high)))

        #: check ingredients
        fresh_ingredients = 0
        for ingredient in ingredients:
            fresh_ingredients += 1 if self.BST.id_in_range(self.Root, int(ingredient)) else 0
        return fresh_ingredients
    
    @timeExecution("Task Two")
    def TaskTwo(self):
        self.BST = BST(None) #: Reset to have build be added in time
        self.Root = self.BST.Root #: Reset Root

        #: Parse input
        database, ingredients = self.InputData.split("\n\n")
        database    = database.split("\n")
        ingredients = ingredients.split("\n")
        
        #: Make BST
        for data in database:
            low, high = data.split("-") 
            self.Root = self.BST.insert(self.Root, (int(low), int(high)))

        #: check ranges
        return self.BST.get_tree_range(self.Root)

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")
