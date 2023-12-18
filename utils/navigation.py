def north(point, distance=1):
    x, y = point
    return (x, y - distance)


def east(point, distance=1):
    x, y = point
    return (x + distance, y)


def south(point, distance=1):
    x, y = point
    return (x, y + distance)


def west(point, distance=1):
    x, y = point
    return (x - distance, y)


def in_bounds(point, maxes):
    x, y = point
    return x >= 0 and x < maxes[0] and y >= 0 and y < maxes[1]
