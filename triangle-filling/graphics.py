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

    t = (x-x1)/(x2-x1)  # slope of linear interpolation
    C = np.zeros(3)  # Initialize the C color vector
    # Calculating colors at x
    C[0] = abs(C1[0] + t*(C2[0]-C1[0]))
    C[1] = abs(C1[1] + t*(C2[1]-C1[1]))
    C[2] = abs(C1[2] + t*(C2[2]-C1[2]))
    return C


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
    if point1[0] == point2[0]:
        return np.inf
    else:
        return (point1[1]-point2[1])/(point1[0]-point2[0])
    
def on_same_line(verts2d):
    """Locates any two vertices of a triangle being on the same horizontal line
    -----------
    verts2d: 3x2 numpy array 
        The coordinates for the 3 vertices of a triangle
    Returns:
    -----------
    Indexes: 2x1 numpy array or NULL
        The two vertices crossed by a horizontal line, or NULL if none of the vertices is horizontal
    """
    
    if verts2d[0, 1] == verts2d[1, 1]:
        return np.array([0,1])
    elif verts2d[1, 1] == verts2d[2, 1]:
        return np.array([1, 2])
    elif verts2d[0, 1] == verts2d[2, 1]:
        return np.array([0, 2])
    else:
        return 'No vertices found'

def find_active_edges(y, verts2d):
    """Finds active edges of a triangle
    -----------
    y: int
        The y coordinate of the current scan line 
        
    verts2d: 3x2 numpy array 
        The coordinates for the 3 vertices of a triangle
    Returns:
    -----------
    Edges: a dictionary key tuple
        The active triangle edges
    """
    y_cord = verts2d[:,1]
    if y in range(y_cord[0], y_cord[1]) and y in range(y_cord[1], y_cord[2]):
        return ('AB', 'BC')
    elif y in range(y_cord[0], y_cord[1]) and y in range(y_cord[0], y_cord[2]):
        return ('AB', 'AC')
    elif y in range(y_cord[1], y_cord[2]) and y in range(y_cord[0], y_cord[2]):
        return ('BC', 'AC')


def find_active_points(y, vert1, vert2, slopes, active_edges):
    """Finds active points in scanline algorithm
    -----------
    y: int
        The y coordinate of the current scan line

    vert1: 2x2 numpy array
        The coordinates of the points creating active edge 1
    
    vert2: 2x2 numpy array
        The coordinates of the points creating active edge 2
    Returns:
    -----------
    Active_points: 2x1 numpy array 
        the range of x, defining the active points
        
    """
    b1 = (vert1[0,0]*vert1[1,1] - vert1[1,0]*vert1[1,1])/(vert1[0,0] - vert1[1,0])
    b2 = (vert2[0, 0]*vert2[1, 1] - vert2[1, 0] * vert2[1, 1])/(vert2[0, 0] - vert2[1, 0])

    x1 = (y-b1)/slopes[active_edges[0]]
    x2 = (y-b2)/slopes[active_edges[1]]

    active_points = [x1, x2]
    return active_points.sort()
    
    

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
                The triagle is colored with a single color, the mean of the vertice's RGB values
            ~GOURAUD:
                Each pixel inside the triangle is colored based on its position using linear color interpolation
    Returns:
    -----------
    Y: MxNx3 numpy array
        The final image with the every point of the triangle colored, covering any pre-existing triangle sharing
        a segmentNotImplemented
    """
    if shade_t == 'FLAT':
        C = np.mean(vcolors, axis=0)
        min_y = min(verts2d[:, 1])
        max_y = max(verts2d[:, 1])
        verts2d = verts2d[verts2d[:, 0].argsort()] #sort vertices by x
        
        #Locating Triangle Lines
        slopes = { 'AB':slope(verts2d[0,:], verts2d[1,:]),
                   'BC':slope(verts2d[1,:], verts2d[2,:]),
                   'AC':slope(verts2d[0,:], verts2d[2,:])
                }
        vertices = {'AB': np.array([verts2d[0, :], verts2d[1, :]]),
                    'BC': np.array([verts2d[1, :], verts2d[2, :]]),
                    'AC': np.array([verts2d[0, :], verts2d[2, :]])}

        if np.unique(verts2d[:, 1]) == len(verts2d):
            active_edges = find_active_edges(min_y+1, verts2d)
            active_points = find_active_points(y, vertices[active_edges[0]], vertices[active_edges[1]], slopes, active_edges)
            for y in range(min_y, max_y):
                for x in range(active_points[0], active_points[1]):
                    img[y][x][:] = C
        
    return img





    elif shade_t == 'GOURAUD':
        raise NotImplemented
