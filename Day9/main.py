import time
from pathlib import Path
from functools import wraps

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

class Point:  # Task 1
    def __init__(self, col, row) -> None:
        self.X = col
        self.Y = row

    def calc_area(self, P: "Point"):
        dx = abs(self.X - P.X) + 1
        dy = abs(self.Y - P.Y) + 1
        return dx * dy

class Line:
    def __init__(self, start: Point, end: Point):
        SX, SY = (start.X, start.Y)
        EX, EY = (end.X, end.Y)
        self.Start = (SX, SY)
        self.End   = (EX, EY)
        self.Orientation = "Vertical" if SX == EX else "Horizontal"
        self.Prev = None
        self.Next = None

class Solution:
    def __init__(self) -> None:
        with open(Path(__file__).parent / "input.txt") as file:
            self.InputData = file.read().strip()

    @timeExecution("Task One")
    def TaskOne(self):
        self.Points = {}
        self.Distances = {}

        #: Make points (the tiles)
        for tile_idx, tile in enumerate(self.InputData.split("\n")):
            x, y = tile.split(",")
            self.Points[tile_idx] = Point(int(x), int(y))

            #: Add areas for each combination of 2 points
            for idx in range(tile_idx, 0, -1):
                point_1 = self.Points[tile_idx]
                assert isinstance(point_1, Point)

                point_2 = self.Points[idx - 1]
                assert isinstance(point_2, Point)

                area = point_1.calc_area(point_2)
                self.Distances[(tile_idx, idx - 1)] = {
                    "points": (point_1, point_2),
                    "area": area
                }

        sorted_distances = list(
            sorted(
                self.Distances.items(),
                key=lambda item: item[1]["area"],
                reverse=True
            )
        )
        _, points = sorted_distances[0]
        return points.get("area")

    @timeExecution("Task Two")
    def TaskTwo(self):
    #: Helpers
        def check_square_cornors(corners: list[tuple[int, int]]):
            xs = [x for x, _ in corners]
            ys = [y for _, y in corners]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            for y in range(min_y, max_y + 1):
                #: Early guard statement
                if y not in self.Valid_vertical and y not in self.Valid_horizontal:
                    return False

                intervals = []
                if y in self.Valid_vertical:
                    for a, b in self.Valid_vertical[y]:
                        intervals.append((min(a, b), max(a, b)))
                if y in self.Valid_horizontal:
                    for a, b in self.Valid_horizontal[y]:
                        intervals.append((min(a, b), max(a, b)))

                intervals.sort()

                #: Merge multiple intervals if needed
                merged_intervals = []
                current_start, current_end = intervals[0]

                for interval_start, interval_end in intervals[1:]:
                    if interval_start <= current_end:
                        if interval_end > current_end:
                            current_end = interval_end
                    else:
                        merged_intervals.append((current_start, current_end))
                        current_start, current_end = interval_start, interval_end

                merged_intervals.append((current_start, current_end))


                interval_covers_rectangle = False
                for interval_start, interval_end in merged_intervals:
                    if interval_start <= min_x and max_x <= interval_end:
                        interval_covers_rectangle = True
                        break

                if not interval_covers_rectangle:
                    return False
            return True

        def check_all_points(point1: Point, point2: Point) -> bool:
            min_x = min(point1.X, point2.X)
            max_x = max(point1.X, point2.X)
            min_y = min(point1.Y, point2.Y)
            max_y = max(point1.Y, point2.Y)

            for y in range(min_y, max_y + 1):
                if y not in self.Valid_vertical and y not in self.Valid_horizontal:
                    return False

                intervals = []
                #: find valid ranges and save them
                if y in self.Valid_vertical:
                    for a, b in self.Valid_vertical[y]:
                        intervals.append((min(a, b), max(a, b)))
                if y in self.Valid_horizontal:
                    for a, b in self.Valid_horizontal[y]:
                        intervals.append((min(a, b), max(a, b)))

                intervals.sort()
                
                #: Merge ranges if needed
                merged_intervals = []
                current_start, current_end = intervals[0]

                for interval_start, interval_end in intervals[1:]:
                    if interval_start <= current_end:
                        if interval_end > current_end:
                            current_end = interval_end
                    else:
                        merged_intervals.append((current_start, current_end))
                        current_start, current_end = interval_start, interval_end

                merged_intervals.append((current_start, current_end))

                rectangle_fits_in_row = False
                for interval_start, interval_end in merged_intervals:
                    if interval_start <= min_x and max_x <= interval_end:
                        rectangle_fits_in_row = True
                        break

                if not rectangle_fits_in_row:
                    return False

                return True

    #: Code entry 
        self.Valid_vertical = {}
        self.Valid_horizontal = {}

        boundary_points: list[Point] = []
        for tile_idx, tile in enumerate(self.InputData.split("\n")):
            x, y = tile.split(",")
            boundary_points.append(Point(int(x), int(y)))

        #: Make boundries
        edges = []
        n = len(boundary_points)
        for i in range(n):
            p = boundary_points[i]
            q = boundary_points[(i + 1) % n]
            edges.append((p, q))

        min_y = min(p.Y for p in boundary_points)
        max_y = max(p.Y for p in boundary_points)

        #: Make verticals 
        for y in range(min_y, max_y + 1):
            xs_v = []
            xs_h = []

            for p, q in edges:
                x1, y1 = p.X, p.Y
                x2, y2 = q.X, q.Y

                if x1 == x2:
                    ymin_e = min(y1, y2)
                    ymax_e = max(y1, y2)
                    if ymin_e <= y < ymax_e:
                        xs_v.append(x1)

                if y1 == y2 == y:
                    xs_h.append((min(x1, x2), max(x1, x2)))

            if xs_v:
                xs_v.sort()
                ranges = []
                for i in range(0, len(xs_v), 2):
                    if i + 1 < len(xs_v):
                        ranges.append((xs_v[i], xs_v[i+1]))
                if ranges:
                    self.Valid_vertical[y] = ranges

            if xs_h:
                self.Valid_horizontal[y] = xs_h

        points = boundary_points

        #: Calc areas for every combination of 2 points
        self.Distances = {}
        for tile_idx, tile in enumerate(points):
            for idx in range(tile_idx, 0, -1):
                p1 = points[tile_idx]
                p2 = points[idx - 1]

                area = p1.calc_area(p2)
                self.Distances[(tile_idx, idx - 1)] = {
                    "points": (p1, p2),
                    "area": area
                }

        sorted_distances = list(
            sorted(
                self.Distances.items(),
                key=lambda item: item[1]["area"],
                reverse=True
            )
        )

        #: Finally go through all squares and check from biggest to lowest 
        for square in sorted_distances:
            _, d = square
            p1, p2 = d["points"]

            corners = [
                (p1.X, p1.Y),
                (p2.X, p2.Y),
                (p1.X, p2.Y),
                (p2.X, p1.Y)
            ]

            if check_square_cornors(corners):
                if check_all_points(p1, p2):
                    return d["area"] #: return first valid square found

if __name__ == "__main__":
    solution = Solution()
    print(f"Answer for Task 1 is: {solution.TaskOne()}\n")
    solution = Solution()
    print(f"Answer for Task 2 is: {solution.TaskTwo()}")
