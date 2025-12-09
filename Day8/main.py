import time, math
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

class Point():
    def __init__(self, x: int, y: int, z: int) -> None:
        self.X = x
        self.Y = y
        self.Z = z

    def dist(self, p: "Point"):
        """Calc and return the distance from this point to another"""
        dx = (self.X - p.X) ** 2
        dy = (self.Y - p.Y) ** 2
        dz = (self.Z - p.Z) ** 2

        return math.sqrt(dx + dy + dz)

#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read()

    @timeExecution("Task One")
    def TaskOne(self):
        self.Points: dict[int, Point] = {}
        
        #: All_distances take a tuple of (row_point_idx, other_point_idx) = dict of {"points" or "dist"} that each contain the ladder
        self.All_distances: dict[tuple[int, int], dict[str, tuple[Point, Point] | float]] = {}
        points_length = 0

        #: parse input
        for point in self.InputData.split("\n"):
            #: Make point
            x, y, z = point.split(",")
            self.Points[points_length] = Point(int(x), int(y), int(z))


            #: add to length and make distances
            for idx in range(points_length, 0, -1):
                point_1 = self.Points[points_length]
                assert isinstance(point_1, Point)

                point_2 = self.Points[idx - 1]
                assert isinstance(point_2, Point)

                dist = abs(point_1.dist(point_2))
                self.All_distances[(points_length, idx - 1)] = {
                    "points"    : (point_1, point_2),
                    "dist"      : dist
                }
            points_length += 1

        #: Sort by distances
        sorted_distances = list(
            sorted(
                self.All_distances.items(),
                key=lambda item: item[1]["dist"]
            )
        )
        
        #: Add cicuits together
        circuits = []
        for i in range(1000):
            ((idx, idy), points_dict) = sorted_distances[i]
            #: is circuit empty? (first iteration)
            if len(circuits) == 0:
                circuits.append(set())
                circuits[0].add(idx)
                circuits[0].add(idy)
                continue

            #: Check if points are in any set already
            found_in_circuit = False
            circuit_idx_it_was_found_in = None
            for i, circuit in enumerate(circuits): 
                #: Check if idx or idy is in the circuit                
                if (idx in circuit or idy in circuit) and not found_in_circuit:
                    circuit.add(idx)
                    circuit.add(idy)
                    found_in_circuit = True
                    circuit_idx_it_was_found_in = i

                #: if idx or idy is in circuit BUT they was already added to another circuit, merge sets
                elif (idx in circuit or idy in circuit) and found_in_circuit:
                    assert isinstance(circuit_idx_it_was_found_in, int)
                    circuits[i] = circuits[circuit_idx_it_was_found_in] | circuit
                    circuits.pop(circuit_idx_it_was_found_in)
                    break

            if not found_in_circuit:
                circuits.append(set())
                circuits[-1].add(idx)
                circuits[-1].add(idy)
        
        #: Count junctions in circuits
        junctions_count = [len(circuit) for circuit in circuits]
        junctions_count.sort(reverse=True)

        return math.prod(junctions_count[:3])


    @timeExecution("Task Two")
    def TaskTwo(self):
        self.Points: dict[int, Point] = {}

        #: All_distances take a tuple of (row_point_idx, other_point_idx) = dict of {"points" or "dist"} that each contain the ladder
        self.All_distances: dict[tuple[int, int], dict[str, tuple[Point, Point] | float]] = {}
        self.All_indexs = set()
        points_length = 0

        #: parse input
        for point in self.InputData.split("\n"):
            #: Make point
            x, y, z = point.split(",")
            self.Points[points_length] = Point(int(x), int(y), int(z))
            self.All_indexs.add(points_length)

            #: add to length and make distances
            for idx in range(points_length, 0, -1):
                point_1 = self.Points[points_length]
                assert isinstance(point_1, Point)

                point_2 = self.Points[idx - 1]
                assert isinstance(point_2, Point)

                dist = abs(point_1.dist(point_2))
                self.All_distances[(points_length, idx - 1)] = {
                    "points"    : (point_1, point_2),
                    "dist"      : dist
                }
            points_length += 1

        #: Sort by distances
        sorted_distances = list(
            sorted(
                self.All_distances.items(),
                key=lambda item: item[1]["dist"]
            )
        )

        #: Add cicuits together
        circuits = []
        for ((idx, idy), points_dict) in sorted_distances:
            #: is circuit empty? (first iteration)
            if len(circuits) == 0:
                circuits.append(set())
                circuits[0].add(idx)
                circuits[0].add(idy)
                continue

            #: Check if points are in any set already
            found_in_circuit = False
            circuit_idx_it_was_found_in = None
            for i, circuit in enumerate(circuits): 
                #: Check if idx or idy is in the circuit                
                if (idx in circuit or idy in circuit) and not found_in_circuit:
                    circuit.add(idx)
                    circuit.add(idy)
                    found_in_circuit = True
                    circuit_idx_it_was_found_in = i

                #: if idx or idy is in circuit BUT they was already added to another circuit, merge sets
                elif (idx in circuit or idy in circuit) and found_in_circuit:
                    assert isinstance(circuit_idx_it_was_found_in, int)
                    circuits[i] = circuits[circuit_idx_it_was_found_in] | circuit
                    circuits.pop(circuit_idx_it_was_found_in)
                    break

            if not found_in_circuit:
                circuits.append(set())
                circuits[-1].add(idx)
                circuits[-1].add(idy)

            #: Added a check for when all points are in the current and only circuit
            if len(circuits) == 1 and self.All_indexs in circuits:
                point1, point2 = points_dict.get("points")
                return point1.X * point2.X
        

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")
