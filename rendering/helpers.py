import numpy as np
from numpy import linalg as la

inside = lambda x, y, slopes, b: False if slopes[0] * x + y + b[0] < 0 and slopes[1] * x + y + b[1] < 0 and slopes[
    2] * x + y + b[2] < 0 else True


def slope(point1, point2):
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
    np.seterr(divide='ignore')
    if point1[0] == point2[0]:
        return np.inf
    else:
        return (point1[1] - point2[1]) / (point1[0] - point2[0])


def interpolate_color(x1, x2, x, C1, C2):
    """Interpolates color C1, C2 of points x1 and x2 to calculate color C of point x
    Parameters:
    -----------
    x1: int
        A coordinate of vertice 1 (horizontal or vertical) of a triangle
    x2: int
        A coordinate of vertice 2 (horizontal or vertical) of a triangle
    x: int
        Α coordinate of the point where we want the color to be calculated
    C1: 3x1 numpy array
        The color at x1
    C2: 3x1 numpy array
        The color at x2
    Returns:
    -----------
    C: 3x1 numpy array
        Color at x
    """
    if x1 == x2:
        return C1
    t = (x - x1) / (x2 - x1)  # slope of linear interpolation
    C = np.zeros(3)  # Initialize the C color vector
    # Calculating colors at x
    C[0] = abs(C1[0] + t * (C2[0] - C1[0]))
    C[1] = abs(C1[1] + t * (C2[1] - C1[1]))
    C[2] = abs(C1[2] + t * (C2[2] - C1[2]))
    return C


def interpolate_vector(x1, x2, x, vector1, vector2):
    """Interpolates color C1, C2 of points x1 and x2 to calculate color C of point x
    Parameters:
    -----------
    x1: int
        A coordinate of vertice 1 (horizontal or vertical) of a triangle
    x2: int
        A coordinate of vertice 2 (horizontal or vertical) of a triangle
    x: int
        Α coordinate of the point where we want the color to be calculated
    C1: 3x1 numpy array
        The color at x1
    C2: 3x1 numpy array
        The color at x2
    Returns:
    -----------
    C: 3x1 numpy array
        Color at x
    """
    if abs(x1 - x2) < 1e-3:
        return vector1
    t = (x - x1) / (x2 - x1)  # slope of linear interpolation
    vector = np.array(vector1 + t * (vector2 - vector1))
    vector /= la.norm(vector)
    return vector


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
        n1 = 1
    else:
        x1 = edges[active_edges[0]].verts[0, 0]
        C1 = edges[active_edges[0]].colors[0, :]
        n1 = 0
    if edges[active_edges[1]].verts[0, 1] == edges[active_edges[1]].y_max:
        x2 = edges[active_edges[1]].verts[1, 0]
        C2 = edges[active_edges[1]].colors[1, :]
        n2 = 1
    else:
        x2 = edges[active_edges[1]].verts[0, 0]
        C2 = edges[active_edges[1]].colors[0, :]
        n2 = 0
    return x1, x2, C1, C2, n1, n2


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


def rasterize(verts_2d, img_h, img_w, cam_h, cam_w):
    """
    Takes every projected point from the camera's shutter and places them in a digital photo.
    Args:
        verts_2d: a Nx3 matrix containing every projected point
        img_h: The height of the image, measured in pixels
        img_w: The width of the image, measured in pixels
        cam_h: The height of the camera, measured in world units
        cam_w: The width of the camera, measured in world units

    Returns:
        verts_rast: projected points placed in a canvas
    """

    verts_rast = np.zeros((len(verts_2d), 2))
    width = img_w / cam_w
    height = img_h / cam_h
    for i in range(len(verts_2d)):
        verts_rast[i, 0] = np.around((verts_2d[i, 0] + cam_h / 2) * height - 0.5)
        verts_rast[i, 1] = np.around((verts_2d[i, 1] + cam_w / 2) * width - 0.5)

    return verts_rast


def calculate_normals(vertices, face_indices):
    """
    Calculates the normal surface vectors

    :param vertices: a 3 × N matrix with the coordinates of the vertices of the object.
    :param face_indices: a 3×N matrix describing the triangles
    :return: A 3 × N matrix with the coordinates of the vertical vectors in each point (vertex) of the surface defining the object
    """

    N_vectors = np.zeros(vertices.shape)

    for face_index in face_indices:
        triangle = vertices[face_index]
        triangle_side_AB = (triangle[1] - triangle[0]) / la.norm((triangle[1] - triangle[0]))
        triangle_side_AC = (triangle[2] - triangle[0]) / la.norm((triangle[2] - triangle[0]))
        triangle_normal_vector = np.cross(triangle_side_AC, triangle_side_AB)
        N_vectors[face_index] += triangle_normal_vector

    for i in range(len(N_vectors)):
        N_vectors[i] /= la.norm(N_vectors[i])
    return N_vectors
