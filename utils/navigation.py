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