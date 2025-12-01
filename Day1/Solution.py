import time
from pathlib import Path

#: HELPER CLASS'
class Node:
    def __init__(self, value) -> None:
        self.Left  = None
        self.Right = None
        self.Value = value
        self.Visited = 0

class LinkedList:
    def __init__(self) -> None:
        self.Root = None
        self.ZeroNode = None

    def make(self, size, root):
        self.Nodes = [Node(i) for i in range(size)]

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

        self.DialPointer = 50
        self.Dial: dict[int, int] = {}
        for i in range(100):
            self.Dial[i] = 0

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
    #: Setup, not timed
    setup_time = time.time()
    solution = Solution()
    print(f"Setup time took: {time.time() - setup_time}")
    startTime = time.time()


    #:Task one
    print(f"Solved task 1: {solution.TaskOne()}, Took: {time.time() - startTime}")
    taskOneTime = time.time()

    #: Task two
    ###: Reset from task one
    solution = Solution()
    print(f"Solved task 2: {solution.TaskTwo()}, Took: {time.time() - taskOneTime}")