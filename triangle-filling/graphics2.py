import helpers as h
import numpy as np

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
    if np.all(verts2d[:,0] == verts2d[0,0]) and np.all(verts2d[:,1] == verts2d[0,1]):
        x = verts2d[0,0]
        y = verts2d[0,1]
        img[x,y] = np.mean(vcolors, axis = 1)
        return img
    verts2d = verts2d[verts2d[:, 1].argsort()]
    edges = {   "AB": np.array([verts2d[0,:], verts2d[1,:]]),
                "AC": np.array([verts2d[0,:], verts2d[2,:]]),
                "BC": np.array([verts2d[1,:], verts2d[2,:]])
            } #Dictionary with points of every edge
    slope = {  "AB": h.slope(verts2d[0,:], verts2d[1,:]),
                "AC": h.slope(verts2d[0,:], verts2d[2,:]),
                "BC": h.slope(verts2d[1,:], verts2d[2,:])
            } #Dictionary with slopes of every edge
    min_limits = {  "AB": np.min([verts2d[0,:], verts2d[1,:]], axis = 0),
                    "AC": np.min([verts2d[0,:], verts2d[2,:]], axis = 0),
                    "BC": np.min([verts2d[1,:], verts2d[2,:]], axis = 0)
            } #Dictionary with min x and y for every edge
    max_limits = {  "AB": np.array([verts2d[0,:], verts2d[1,:]], axis = 0),
                    "AC": np.array([verts2d[0,:], verts2d[2,:]], axis = 0),
                    "BC": np.array([verts2d[1,:], verts2d[2,:]], axis = 0)
                } #dictionary with max x and y for every edge
    y_min = verts2d[0,1]
    y_max = verts2d[1,1]
    flat_color = np.mean(vcolors, axis = 1)
    for y in range(y_min, y_max):
        (active_edge1, active_edge2) = h.find_edges(y, (min_limits, max_limits))
        x1 = x2 = h.find_active_point()
    return img

def render(verts2d, faces, vcolors, depth, shade_t="FLAT"):
    if shade_t not in ['FLAT', 'GOURAUD']:
        print("Mode not found")
        return 
    M = N = 512
    image_shape = (M,N,3)
    img = np.ones(image_shape).astype(int)
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


