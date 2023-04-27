import math

import laspy


def normalize_vector(vector):
    x, y, z = vector
    length = math.sqrt(x * x + y * y + z * z)
    return [x / length, y / length, z / length]


def las_convert(filename):
    with laspy.open(filename) as f:
        las = f.read()
        points = las.xyz

    return list(points)
