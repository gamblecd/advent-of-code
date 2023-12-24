from time import time
import os
import heapq


def get_input_file(args, script_dir, filename=None):
    if filename:
        return os.path.join(script_dir, "inputs", "actual.txt")
    run_actual = len(args) >= 1 and args[0] == "PROD"
    if run_actual:
        filename = os.path.join(script_dir, "inputs", "actual.txt")
    else:
        filename = os.path.join(script_dir, "inputs", "ex.txt")
    return filename


def timer_func(f=None, print_args=False):
    # This function shows the execution time of
    # the function object passed
    def decorator(func):
        def wrap_func(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            if print_args:
                print(
                    f'Function {func.__name__!r}, ({", ".join(map(str,args))}) executed in {(t2-t1):.4f}s'
                )
            else:
                print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
            return result

        return wrap_func
    return decorator(f) if callable(f) else decorator


def print_grid_basic(grid, sep=" "):
    for x in grid:
        print(*x, sep=sep)


def print_grid(min, max, basic_char, overlays):
    xmin, ymin = min
    xmax, ymax = max

    offset = min  # TODO genericize this

    grid = [[basic_char for _ in range(xmin, xmax + 1)] for _ in range(ymin, ymax + 1)]

    # add overlays:
    for overlay in overlays:
        char, lst = overlay
        for point in lst:
            x = point[0] - offset[0]
            y = point[1] - offset[1]
            if callable(char):
                grid[y][x] = char(point)
            else:
                grid[y][x] = char

    # Build Index Row (max 99)
    x_lines = [["    "] for i in range((xmax + 1) // 10)]
    if len(x_lines) >= 2:
        for i in range(xmin, xmax + 1):
            ones = x_lines[-1]
            if i % 5 == 0:
                if i < 0:
                    ones[-1] = "-"
                ones.append(str(i % 10))
                if i >= 10:
                    x_lines[-2].append(str(i // 10))
                else:
                    x_lines[-2].append(" ")
            else:
                for line in x_lines:
                    line.append(" ")
        for line in x_lines:
            print("".join(line))

    y_index = ymin
    for y in grid:
        ## insert y index col (max 99)
        print(str(y_index).rjust(3) + " " + "".join(y))
        y_index += 1


def BFS_search(
    initial,
    getHeapItem=lambda x: x,
    end_condition=lambda x: len(x.children) == 0,
    returner=lambda x, y, z: x,
    getChildren=lambda x: x.children,
    getVisitor=lambda x: x,
    getWeight=lambda x: x.weight,
):
    visited = []
    start = (0, getHeapItem(initial), visited)
    paths = []
    Q = []
    heapq.heappush(Q, start)
    while Q:
        weight, item, visited = heapq.heappop(Q)
        if end_condition(item):
            paths.append(returner(item, weight, visited))
        for child in getChildren(item):
            visitor = getVisitor(child)
            if visitor in visited:
                continue
            else:
                new_item = getHeapItem(child)
                new_weight = weight + getWeight(child)
                heapq.heappush(Q, (new_weight, new_item, visited + [visitor]))
    return paths
