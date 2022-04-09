from cmath import isnan
from pickle import FALSE
from turtle import color

from pyparsing import null_debug_action
import helpers as h
import numpy as np

class Edge:
    def __init__(self, name, start, end, color_start, color_end, slope, is_active):
        self.name = name
        self.start = start
        self.end = end
        self.color_start = color_start
        self.color_end = color_end
        self.slope = slope
        self.is_active = is_active;
        self.y_min = min(start[1], end[1])
        self.y_max = max(start[1], end[1])
        
        

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
    
    t = (x-x1)/(x2-x1) # slope of linear interpolation
    C = np.zeros(3)  # Initialize the C color vector
    # Calculating colors at x
    C[0] = abs(C1[0] + t*(C2[0]-C1[0]))
    C[1] = abs(C1[1] + t*(C2[1]-C1[1]))
    C[2] = abs(C1[2] + t*(C2[2]-C1[2]))
    return C

def shade_triangle(img, verts2d, vcolors, shade_t='FLAT'):
    """Calculates color of a triange with 2 different ways
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
    if np.all(verts2d[:,0] == verts2d[0,0]) and np.all(verts2d[:,1] == verts2d[0,1]):
        x = verts2d[0,0]
        y = verts2d[0,1]
        img[x,y] = np.mean(vcolors, axis = 0)
        return img
    if len(np.unique(verts2d)) < 3:
        img = bresenham(img, np.unique(verts2d), vcolors, shade_t)


    verts2d = verts2d[verts2d[:, 1].argsort()]

    Edge1 = Edge("AB", verts2d[0,:], verts2d[1,:], 
                vcolors[0,:], vcolors[1,:], 
                h.slope(verts2d[0,:], verts2d[1,:]), False)
    Edge2 = Edge("BC", verts2d[1,:], verts2d[2,:], 
                vcolors[1,:], vcolors[2,:], 
                h.slope(verts2d[1,:], verts2d[2,:]), False)
    Edge3 = Edge("AC", verts2d[0,:], verts2d[2,:], 
                vcolors[0,:], vcolors[2,:], 
                h.slope(verts2d[0,:], verts2d[2,:]), False)
    y_max = np.array(np.max(verts2d, axis=0))[1]
    y_min = np.array(np.min(verts2d, axis=0))[1]

    horizontal_line = False
    edges = [Edge1, Edge2, Edge3]
    if np.isnan(np.sum([Edge1.slope, Edge2.slope, Edge3.slope])):
        return img

    for edge in edges:
        if y_min == edge.y_min:
            if edge.slope != 0:
                edge.is_active = True;
        else:
            horizontal_line = True
    
    active_edges = [edge for edge in edges if edge.is_active]
    if not horizontal_line:
        for vert in verts2d:
            if vert[1] == y_min:
                x1 = vert[0]
                x2 = x1+0.5
        img[x1, y_min] = np.mean(vcolors, axis = 0)
    else:
        x1, x2, C1, C2 = h.find_active_points(active_edges)
        for x in range(x1,x2+1):
            if shade_t == 'FLAT':
                img[x,y_min] = np.mean(vcolors, axis = 0)
            else:
                img[x,y_min] = interpolate_color(x1, x2, x, C1, C2)

    for y in range(y_min+1, y_max+1):
        x1 = x1 + 1/active_edges[0].slope
        x2 = x2 + 1/active_edges[1].slope
        
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        color_A = interpolate_color(active_edges[0].y_min, active_edges[0].y_max, y, active_edges[0].color_start, active_edges[0].color_end)
        color_B = interpolate_color(active_edges[1].y_min, active_edges[1].y_max, y, active_edges[1].color_start, active_edges[1].color_end)
        for x in range(int(x_min), int(x_max)+1):
            if shade_t == 'GOURAUD':
                img[x,y] = interpolate_color(x1, x2, x, color_A, color_B)
            else:
                img[x,y] = np.mean(vcolors, axis = 0) 
        active_edges = h.update_edges(y, edges, active_edges)
        
    return img
    
    
    
    

def render(verts2d, faces, vcolors, depth, shade_t="FLAT"):
    if shade_t not in ['FLAT', 'GOURAUD']:
        print("Mode not found")
        return 
    M = N = 512
    image_shape = (M,N,3)
    img = np.ones(image_shape)
    #Average depth of every triangle
    depth_order = np.array(np.mean(depth[faces], axis = 1))
    #Sort triangles by depth
    sorted_triangles = list(np.flip(np.argsort(depth_order)))
    for triangles in sorted_triangles:
        triangle_vertices_indeces = faces[triangles]
        triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
        triangle_vcolors = np.array(vcolors[triangle_vertices_indeces])
        img = shade_triangle(img ,triangle_verts2d, triangle_vcolors, shade_t)
    return img

def bresenham(img, verts2d, vcolors, shade_t):
    x1, y1 = verts2d[1,:]
    x2, y2 = verts2d[2,:]
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)
    y=y1
    for x in range(x1,x2+1):
        # Add slope to increment angle formed
        slope_error_new =slope_error_new + m_new
 
        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y=y+1
            slope_error_new =slope_error_new - 2 * (x2 - x1)
        if(shade_t == 'GOURAUD'):
            img[x,y] = interpolate_color(y1, y2, y, vcolors[0,:], vcolors[1,:])
        else:
            img[x,y] = np.mean(vcolors, axis = 0) 