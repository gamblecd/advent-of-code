def north(point):
    x,y = point
    return (x, y-1)
def east(point):
    x,y = point
    return (x+1,y)
def south(point):
    x,y = point
    return (x, y+1)
def west(point):
    x,y = point
    return (x-1, y)
def in_bounds(point, maxes):
    x,y = point
    return x >= 0 and x< maxes[0] and y >=0 and y<maxes[1]
