from time import time
import os
def get_input_file(args, script_dir, filename=None):
    
    if filename:
        return  os.path.join(script_dir, "inputs", "actual.txt")
    run_actual = len(args) >= 1 and args[0] == "PROD"
    if (run_actual):
        filename = os.path.join(script_dir, "inputs", "actual.txt")
    else:
        filename = os.path.join(script_dir, "inputs", "ex.txt")
    return filename


def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def timer_func_with_args(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r}, ({", ".join(map(str,args))}) executed in {(t2-t1):.4f}s')
        return result
    return wrap_func
def print_grid(grid, sep=" "):
    for x in grid:
        print(*x, sep=sep);
