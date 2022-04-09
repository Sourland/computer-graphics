import numpy as np
import helpers as h
import threading

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
    if len(np.unique(verts2d)) < 3:
        return img
    verts2d = verts2d[verts2d[:, 1].argsort()]
    x_max = np.array(np.max(verts2d, axis=0))[0]
    x_min = np.array(np.min(verts2d, axis=0))[0]
    y_max = np.array(np.max(verts2d, axis=0))[1]
    y_min = np.array(np.min(verts2d, axis=0))[1]
    
    if shade_t == 'GOURAUD':
        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max+1):
                (a,b,c) = h.compute_barycentric_coordinates(verts2d, x, y)
                if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
                    img[x,y,0] = a*vcolors[0,0] + b*vcolors[1,0] + c*vcolors[2,0]
                    img[x,y,1] = a*vcolors[0,1] + b*vcolors[1,1] + c*vcolors[2,1]
                    img[x,y,2] = a*vcolors[0,2] + b*vcolors[1,2] + c*vcolors[2,2]
    else:
        flat_color = np.mean(vcolors, axis = 0)
        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max+1):
                (a,b,c) = h.compute_barycentric_coordinates(verts2d, x, y)
                if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
                    img[x,y] = flat_color


    return img


        
def active_points(y, verts2d, edges):
    slope1 = h.slope(verts2d[edges[0][0],:],verts2d[edges[0][1],:])
    slope2 = h.slope(verts2d[edges[1][0],:],verts2d[edges[1][1],:])
    
    if slope1 == 0:
        return verts2d[edges[0][0],0], verts2d[edges[0][1],0]
    elif slope2 == 0:
        return verts2d[edges[1][0],0], verts2d[edges[1][1],0]
    else:
        node1 = np.where(verts2d[:,1] == max(verts2d[edges[0][0],1],verts2d[edges[0][1],1]))
        node2 = np.where(verts2d[:,1] == max(verts2d[edges[1][0],1],verts2d[edges[1][1],1]))
        x1 = verts2d[node1,0] + abs(verts2d[node1,1]-y) * (1/slope1)
        x2 = verts2d[node2,0] + abs(verts2d[node2,1]-y) * (1/slope2)
        return int(x1), int(x2)


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




    