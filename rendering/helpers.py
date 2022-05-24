import numpy as np

inside = lambda x, y, slopes, b: False if slopes[0] * x + y + b[0] < 0 and slopes[1] * x + y + b[1] < 0 and slopes[
    2] * x + y + b[2] < 0 else True


def slope(point1, point2):
    np.seterr(divide='ignore')
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
        return (point1[1] - point2[1]) / (point1[0] - point2[0])


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
    a = f_ab(x, y, 1, 2, verts2d) / f_ab(verts2d[0, 0], verts2d[0, 1], 1, 2, verts2d)
    b = f_ab(x, y, 2, 0, verts2d) / f_ab(verts2d[1, 0], verts2d[1, 1], 2, 0, verts2d)
    c = f_ab(x, y, 0, 1, verts2d) / f_ab(verts2d[2, 0], verts2d[2, 1], 0, 1, verts2d)
    return a, b, c


def f_ab(x, y, a, b, verts2d):
    """A helper function for barycentric coordinates calculation
    """
    return ((verts2d[a, 1] - verts2d[b, 1]) * x +
            (verts2d[b, 0] - verts2d[a, 0]) * y +
            verts2d[a, 0] * verts2d[b, 1] -
            verts2d[b, 0] * verts2d[a, 1])


def find_initial_elements(edges, active_edges):
    """Calculates initial active points and colors
    -----------
    edges: 3x1 Edge array
        All the edge objects
    active_edges: 2x1 index array
        Indexes to the 2 current active edges
    Returns:
    -----------
    x1,x2: int 
        Initial active points
    C1, C2: 3x1 numpy array
        RGB values for initial active_point
    """
    if edges[active_edges[0]].verts[0, 1] == edges[active_edges[0]].y_max:
        x1 = edges[active_edges[0]].verts[1, 0]
        C1 = edges[active_edges[0]].colors[1, :]
    else:
        x1 = edges[active_edges[0]].verts[0, 0]
        C1 = edges[active_edges[0]].colors[0, :]
    if edges[active_edges[1]].verts[0, 1] == edges[active_edges[1]].y_max:
        x2 = edges[active_edges[1]].verts[1, 0]
        C2 = edges[active_edges[1]].colors[1, :]
    else:
        x2 = edges[active_edges[1]].verts[0, 0]
        C2 = edges[active_edges[1]].colors[0, :]
    return x1, x2, C1, C2


def update_active_edges(edges, active_edges, y):
    """Calculates initial active points and colors
    -----------
    edges: 3x1 Edge array
        All the edge objects
    active_edges: 2x1 index array
        Indexes to the 2 current active edges
    y: int
        current y scanline
    Returns:
    -----------
    active_edges:2x1 index array
        The new active edges
    """
    if y == edges[active_edges[0]].y_max:
        for i in range(len(edges)):
            if y == edges[i].y_min:
                active_edges[0] = i
    elif y == edges[active_edges[1]].y_max:
        for i in range(len(edges)):
            if y == edges[i].y_min:
                active_edges[1] = i
    return active_edges


def casting(*args):
    """

    Args:
        *args:

    Returns:

    """
    return tuple(arg for arg in args)


def swap(a, b):
    """

    Args:
        a:
        b:

    Returns:

    """
    temp = a
    a = b
    b = temp
    return a, b
