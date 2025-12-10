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

class Point: #: Task 1 
    def __init__(self, col, row) -> None:
        self.X = col
        self.Y = row

    def calc_area_T1(self, P: "Point"):
        dx = abs(self.X - P.X) + 1
        dy = abs(self.Y - P.Y) + 1
        return dx * dy


#: SOLUTIONS
class Solution:
    def __init__(self) -> None:
        #: Read input
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read()

    @timeExecution("Task One")
    def TaskOne(self):
        self.Points = {}
        self.Distances = {}

        #: Parse input
        for tile_idx, tile in enumerate(self.InputData.split("\n")):
            #: Make point
            x, y = tile.split(",")
            self.Points[tile_idx] = Point(int(x), int(y))

            #: make distances
            for idx in range(tile_idx, 0, -1):
                point_1 = self.Points[tile_idx]
                assert isinstance(point_1, Point)

                point_2 = self.Points[idx - 1]
                assert isinstance(point_2, Point)

                area = point_1.calc_area_T1(point_2)
                self.Distances[(tile_idx, idx - 1)] = {
                    "points"    : (point_1, point_2),
                    "area"      : area
                }

         #: Sort by distances
        sorted_distances = list(
            sorted(
                self.Distances.items(),
                key=lambda item: item[1]["area"],
                reverse=True
            )
        )
        _, points = sorted_distances[0]
        return points.get("area") #: area length times width

    @timeExecution("Task Two")
    def TaskTwo(self):
    #: Helpers 
        def shoelace_area_calc(points: list[Point]):
            points_length = len(points)
            if points_length < 3:
                return 0.0  # not a polygon, area is zero

            area = 0.0
            for i in range(points_length):
                j = (i + 1) % points_length  #: always get next unless i+1 == j then modulo return 0 and you get first element
                p = points[i]
                q = points[j]
                area += (p.X * q.Y) - (p.Y * q.X)
            return abs(area) * 0.5

        #: Storage variables
        self.Points = {}
        self.areas = {}
        
        #: make points
        for tile_idx, tile in enumerate(self.InputData.split("\n")):
            #: Make point
            x, y = tile.split(",")
            self.Points[tile_idx] = Point(int(x), int(y))
        
        #: Go through each point and calc the area of everything without it
        #: Only keep areas that would make the polygon smaller, as any bigger areas are invalid
        original_area = shoelace_area_calc([self.Points[i] for i in self.Points])
        for point_remove_idx in self.Points:
            list_of_points_to_calc_area = [self.Points[i] for i in self.Points if not i == point_remove_idx]
            self.areas[point_remove_idx]= shoelace_area_calc(list_of_points_to_calc_area)
            pass
        pass
            
if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")

    #: Reset from task one
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")
