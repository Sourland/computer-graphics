from distutils.log import error
import numpy as np

inside = lambda x, y, slopes, b: False if slopes[0]*x + y + b[0] < 0 and slopes[1]*x + y + b[1] < 0 and slopes[2]*x + y + b[2] < 0 else True

def slope(point1, point2):
    np.seterr(divide = 'ignore') 
    """Calculates slope of two points
    -----------
    point1:1x2 numpy array
        First point for slope calculation
    point2:1x2 numpy array
        Second point for slope calculation 
    Returns:
    -----------
    Slope: int
        The slope of the line crossing point 1 and 2 
    """
    if point1[0] == point2[0]:
        return np.inf
    else:
        return (point1[1]-point2[1])/(point1[0]-point2[0])

def compute_barycentric_coordinates(verts2d, x, y):
    """Calculates barycentric coordinates of x,y in relationship to verts2d location
    -----------
    verts2d: 3x2 numpy array
        The coordinates of the triangle vertices
    (x,y): int
        The current pixel coordinates
    Returns:
    -----------
    (a,b,c): float
        The barycentric coordinates of the pixel
    """
    a = f_ab(x, y, 1, 2, verts2d) / f_ab(verts2d[0,0], verts2d[0,1], 1, 2, verts2d)
    b = f_ab(x, y, 2, 0, verts2d) / f_ab(verts2d[1,0], verts2d[1,1], 2, 0, verts2d)
    c = f_ab(x, y, 0, 1, verts2d) / f_ab(verts2d[2,0], verts2d[2,1], 0, 1, verts2d)
    return a,b,c

def f_ab(x, y, a, b, verts2d):
    """A helper function for barycentric coordinates calculation
    """
    return ((verts2d[a,1] - verts2d[b,1]) * x + 
    (verts2d[b, 0] - verts2d[a,0]) * y + 
    verts2d[a, 0] * verts2d[b, 1] - 
    verts2d[b, 0] * verts2d[a , 1]) 


