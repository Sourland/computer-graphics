import numpy as np
from numpy import linalg as la
from .light import ambient_light, diffuse_light, specular_light


class Edge:
    def __init__(self, name, verts, colors, slope, is_active):
        self.normal_vectors = None
        self.name = name
        self.verts = verts
        self.colors = colors
        self.slope = slope
        self.is_active = is_active
        self.y_min = min(verts[0, 1], verts[1, 1])
        self.y_max = max(verts[0, 1], verts[1, 1])


    def set_normal_vectors(self, normal_vectors):
        self.normal_vectors = normal_vectors


def slope(pointA, pointB):
    """
    Calculates slope of two points in a 2D Plane

    Args:
        pointA: First point for slope calculation
        pointB: Second point for slope calculation

    Returns:
        the slope of the line AB crossing point A and B
    """

    np.seterr(divide='ignore')
    if pointA[0] == pointB[0]:
        return np.inf
    else:
        return (pointA[1] - pointB[1]) / (pointA[0] - pointB[0])


def interpolate_color(x1, x2, x, C1, C2):
    """
    Interpolates color C1, C2 of points x1 and x2 to calculate color C of point x

    Args:
        x1: A coordinate of vertice 1 (horizontal or vertical) of a triangle
        x2: A coordinate of vertice 2 (horizontal or vertical) of a triangle
        x: A coordinate of the point where we want the color to be calculated
        C1: The color at x1
        C2: The color at x2

    Returns:
        Color at x
    """

    if abs(x1 - x2) < 1e-3:
        return C1
    t = (x - x1) / (x2 - x1)  # slope of linear interpolation
    C = np.zeros(3)  # Initialize the C color vector
    # Calculating colors at x
    C[0] = abs(C1[0] + t * (C2[0] - C1[0]))
    C[1] = abs(C1[1] + t * (C2[1] - C1[1]))
    C[2] = abs(C1[2] + t * (C2[2] - C1[2]))
    return C


def interpolate_vector(x1, x2, x, vector1, vector2):
    """
    Interpolates vectors horizontally or vertically between points A and B
    Args:
        x1: A coordinate value (horizontal or vertical) of point A
        x2: A coordinate value (horizontal or vertical) of point B
        x: A coordinate value (horizontal or vertical) of the desired point
        vector1: The normal vector at point A
        vector2: The normal Vector at point B

    Returns:
        The normal vector at x
    """
    if abs(x1 - x2) < 1e-3:
        return vector1
    t = (x2 - x) / (x2 - x1)  # slope of linear interpolation
    vector = np.array(t * vector1 + (1 - t) * vector2)
    vector /= la.norm(vector)
    return vector


def find_initial_elements(edges, active_edges):
    """
    Calculates initial active points and colors
    Args:
        edges: A list with every edge of a polygon (in this case a triangle)
        active_edges: A list with every active edge in the scanline algorithm of a polygon (in this case a triangle)

    Returns:
        The scanline algorithm starting colors, points and normal vectors.
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
    """
    Changes the current active edges in the scanline algorithm, if required
    Args:
        edges: A list with every edge of a polygon (in this case a triangle)
        active_edges: A list with every active edge in the scanline algorithm of a polygon (in this case a triangle)
        y: The current y-coordinate in the scanline algorithm

    Returns:
        The new list of active edges
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


def swap(object_a, object_b):
    """
    Swaps 2 objects
    Args:
        object_a: First object
        object_b: Second object

    Returns:
        Swapped objects A and B (now B and A)
    """
    temp = object_a
    object_a = object_b
    object_b = temp
    return object_a, object_b


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
        verts_rast[i, 1] = np.around((-verts_2d[i, 1] + cam_w / 2) * width - 0.5)
    return verts_rast


def calculate_normals(vertices, face_indices):
    """
    Calculates the normal surface vectors

    Args:
        vertices: a 3 × N matrix with the coordinates of the vertices of the obje
        face_indices: A 3 × N matrix with the coordinates of the vertical vectors in each point (vertex) of the surface defining the object

    Returns:
        Normal vectors in each triangle vertice
    """

    N_vectors = np.zeros(vertices.shape)

    for face_index in face_indices:
        triangle = vertices[face_index]
        triangle_side_AB = (triangle[0] - triangle[1]) / la.norm((triangle[0] - triangle[1]))
        triangle_side_AC = (triangle[0] - triangle[2]) / la.norm((triangle[0] - triangle[2]))
        triangle_normal_vector = np.cross(triangle_side_AC, triangle_side_AB)
        N_vectors[face_index] += triangle_normal_vector

    for i in range(len(N_vectors)):
        N_vectors[i] /= la.norm(N_vectors[i])
    return N_vectors


def get_color(lighting, P, normal_vector, color, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia):
    """
    Calculates the color of a pixel depending on lighting

    Args:
         lighting: a variable that controls whether all the light sources in the scene will be used, or just one and which one.
         P: a vector of dimension 3×1 contains the barycentre of the triangle before its projection.
         normal_vector: a 3 × 1 vector containing the normal vectors on that point of the 3D triange
         color: a 3 × 1 matrix containing the colour of the point of the 3D triangle.
         cam_pos: a 3 × 1 column vector with the coordinates of the observer (i.e. the camera).
         ka: the factor of diffused light from the environment
         kd: the diffuse reflection coefficient of the Phong model
         ks: the specular reflection coefficient of the Phong model
         n: the Phong coefficient
         light_positions: a list of 3 × 1 vectors containing the components of the position of the light sources.
         light_intensities: a list of 3 × 1 vectors containing the intensities of the bright sources (corresponding to light_positions).
         Ia: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].

    Returns:
        The final color of a pixel
    """

    if lighting == 'Ambient':
        color = ambient_light(ka, Ia)

    if lighting == 'Diffuse':
        color = diffuse_light(P, normal_vector, color, kd, light_positions, light_intensities)

    if lighting == 'Specular':
        color = specular_light(P, normal_vector, color, cam_pos, ks, n, light_positions, light_intensities)

    if lighting == 'All':
        color = ambient_light(ka, Ia) + \
                diffuse_light(P, normal_vector, color, kd, light_positions, light_intensities) + \
                specular_light(P, normal_vector, color, cam_pos, ks, n, light_positions, light_intensities)

    return color
