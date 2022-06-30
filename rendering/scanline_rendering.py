from rendering import helpers as h
import numpy as np
import math


class Edge:
    def __init__(self, name, verts, colors, slope, is_active):
        self.normal_vectors = None
        self.name = name
        self.verts = verts
        self.colors = colors
        self.slope = slope
        self.is_active = is_active;
        self.y_min = min(verts[0, 1], verts[1, 1])
        self.y_max = max(verts[0, 1], verts[1, 1])

    def set_normal_vectors(self, normal_vectors):
        self.normal_vectors = normal_vectors


def interpolate(x1, x2, x, C1, C2):
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


def shade_triangle(img, verts2d, vcolors, shade_t='FLAT'):
    """
    Calculates color of a triange with 2 different ways
    -----------
    img: MxNx3 numpy array 
        An image with possible pre-existing triangles
    verts2d: 3x2 numpy array 
        The coordinates for the 3 vertices of a triangle
    vcolors: 3x3 numpy array
        The color of the vertices in an RGB scale, ranging from [0,1]
    shade_t: string
        The mode of coloring
            ~FLAT: 
                The triangle is colored with a single color, the mean of the vertice's RGB values
            ~GOURAUD:
                Each pixel inside the triangle is colored based on its position using linear color interpolation
    Returns:
    -----------
    Y: MxNx3 numpy array
        The final image with the every point of the triangle colored, covering any pre-existing triangle sharing
        a segmentNotImplemented
    """
    # Check for exception
    if np.all(verts2d[:, 0] == verts2d[0, 0]) and np.all(verts2d[:, 1] == verts2d[0, 1]):
        x = verts2d[0, 0]
        y = verts2d[0, 1]
        img[x, y] = np.mean(vcolors, axis=0)
        return img

    if len(np.unique(verts2d, axis=0)) < 3:
        return img

    # Initialize Edge elements
    Edge1 = Edge("AB", np.array([verts2d[0, :], verts2d[1, :]]),
                 np.array([vcolors[0, :], vcolors[1, :]]),
                 h.slope(verts2d[0, :], verts2d[1, :]), False)
    Edge2 = Edge("BC", np.array([verts2d[1, :], verts2d[2, :]]),
                 np.array([vcolors[1, :], vcolors[2, :]]),
                 h.slope(verts2d[1, :], verts2d[2, :]), False)
    Edge3 = Edge("AC", np.array([verts2d[0, :], verts2d[2, :]]),
                 np.array([vcolors[0, :], vcolors[2, :]]),
                 h.slope(verts2d[0, :], verts2d[2, :]), False)
    # Define minimum and maximum y
    y_max = np.array(np.max(verts2d, axis=0))[1]
    y_min = np.array(np.min(verts2d, axis=0))[1]

    # Initialize search parametrs
    edges = [Edge1, Edge2, Edge3]
    active_edges = []
    horizontal_line = False
    # Begin search for initial elements
    for i in range(len(edges)):
        if y_min == edges[i].y_min:
            if edges[i].slope != 0:
                edges[i].is_active = True;
                active_edges.append(i)
            else:
                horizontal_line = True

    # Act based on active edge findings
    if len(active_edges) < 2:
        return img
    if not horizontal_line:
        for i in range(len(verts2d)):
            if verts2d[i, 1] == y_min:
                index = i
                x1 = verts2d[i, 0]
                x2 = x1
        if 0 <= x1 <= img.shape[0] - 1 and 0 <= y_min <= img.shape[1] - 1:
            img[int(math.floor(x1 + 0.5)), int(math.floor(y_min + 0.5))] = vcolors[index, :]
    else:
        x1, x2, C1, C2, n1, n2 = h.find_initial_elements(edges, active_edges)
        for x in range(x1, x2 + 1):
            if 0 <= x <= img.shape[0] - 1 and 0 <= y_min <= img.shape[1] - 1:
                if shade_t == 'FLAT':
                    img[x, y_min] = np.mean(vcolors, axis=0)
                else:
                    img[x, y_min] = interpolate(x1, x2, x, C1, C2)
    # Individual cases over

    # Begin Scanline Algorithm
    for y in range(y_min + 1, y_max + 1):
        if edges[active_edges[0]].slope != float('inf'):
            x1 = x1 + 1 / edges[active_edges[0]].slope
        if edges[active_edges[1]].slope != float('inf'):
            x2 = x2 + 1 / edges[active_edges[1]].slope
        color_A = interpolate(edges[active_edges[0]].y_min, edges[active_edges[0]].y_max, y,
                                    edges[active_edges[0]].colors[0, :], edges[active_edges[0]].colors[1, :])
        color_B = interpolate(edges[active_edges[1]].y_min, edges[active_edges[1]].y_max, y,
                                    edges[active_edges[1]].colors[0, :], edges[active_edges[1]].colors[1, :])
        for x in range(int(min(x1, x2)), int(max(x1, x2)) + 1):
            if 0 <= x <= img.shape[0] - 1 and 0 <= y <= img.shape[1] - 1:
                if shade_t == 'GOURAUD':
                    img[int(math.floor(x + 0.5)), y] = interpolate(int(x1), int(x2), int(math.floor(x + 0.5)),
                                                                         color_A, color_B)
                else:
                    img[int(math.floor(x + 0.5)), y] = np.mean(vcolors, axis=0)
        active_edges = h.update_active_edges(edges, active_edges, y)
    return img

def render(verts2d, faces, vcolors, depth, shade_t="FLAT"):
    """Renders a full object using triangle_shading
    -----------
    verts2d: Lx2 numpy array
        The coordinates for all points of the object
    faces: Kx3 numpy array:
        A list of vertices for every triangle
    vcolors: Lx3 numpy array
        The color of the vertices in an RGB scale, ranging from [0,1]
    depth: Lx3 numpy array
        The depth of each vertice in the camvas
    shade_t: string
        The mode of coloring
            ~FLAT:
                The triangle is colored with a single color, the mean of the vertice's RGB values
            ~GOURAUD:
                Each pixel inside the triangle is colored based on its position using linear color interpolation
    Returns:
    -----------
    Y: MxNx3 numpy array
        The final image with the every point of the triangle colored, covering any pre-existing triangle sharing
        a segmentNotImplemented
    """
    if shade_t not in ['FLAT', 'GOURAUD']:
        print("Mode not found")
        return
    M = N = 512
    image_shape = (M, N, 3)
    img = np.ones(image_shape)
    # Average depth of every triangle
    depth_order = np.array(np.mean(depth[faces], axis=1))
    # Sort triangles by depth
    sorted_triangles = list(np.flip(np.argsort(depth_order)))
    for triangles in sorted_triangles:
        triangle_vertices_indeces = faces[triangles]
        triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
        triangle_vcolors = np.array(vcolors[triangle_vertices_indeces])
        img = shade_triangle(img, triangle_verts2d, triangle_vcolors, shade_t)
    return img