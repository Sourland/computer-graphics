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

def intercept(slope, point):
    if slope == np.inf:
        return point[0]
    else:
        return point[1] - slope*point[0]

def compute_barycentric_coordinates(verts2d, x, y):
    a = f_ab(x, y, 1, 2, verts2d) / f_ab(verts2d[0,0], verts2d[0,1], 1, 2, verts2d)
    b = f_ab(x, y, 2, 0, verts2d) / f_ab(verts2d[1,0], verts2d[1,1], 2, 0, verts2d)
    c = f_ab(x, y, 0, 1, verts2d) / f_ab(verts2d[2,0], verts2d[2,1], 0, 1, verts2d)
    return a,b,c

def f_ab(x, y, a, b, verts2d):
    return ((verts2d[a,1] - verts2d[b,1]) * x + 
    (verts2d[b, 0] - verts2d[a,0]) * y + 
    verts2d[a, 0] * verts2d[b, 1] - 
    verts2d[b, 0] * verts2d[a , 1]) 

def current_edges(y, verts2d):
    y0, y1, y2 = verts2d[0,1], verts2d[1,1], verts2d[2,1]
    if y0 <= y <= y1 and y0 <= y <= y2:
        return((0,1), (0,2)) 
    elif y1 <= y <= y2 and y0 <= y <= y2:
        return((1,2), (0,2)) 
    elif y1 <= y <= y2 and y0 <= y <= y1:
        return((1,2), (0,1)) 


def find_active_points(edges):
    if edges[0].start[1] == edges[0].y_max:
        x1 = edges[0].end[0]
        C1 = edges[0].color_end
    else:
        x1 = edges[0].start[0]
        C1 = edges[0].color_start
    if edges[1].start[1] == edges[1].y_max:
        x2 = edges[1].end[0]
        C2 = edges[1].color_end
    else:
        x2 = edges[1].start[0]
        C2 = edges[1].color_start
    return x1, x2, C1, C2
    

def update_edges(y, edges, active_edges):
    if y == active_edges[0].y_max:
        for edge in edges:
            if y == edge.y_min:
                active_edges[0] = edge
    elif y == active_edges[1].y_max:
        for edge in edges:
            if y == edge.y_min:
                active_edges[1] = edge
    return active_edges

def update_points(x1, x2, active_edges, current_y):
    y1, y2  =active_edges[0].y_max, active_edges[1].y_max
    x1_end, x2_end = active_edges[1].start[0], active_edges[1].end[0]

    m_new1 = 2*(x1_end-x1)
    m_new2 = 2*(x2_end-x2)
    error1 = m_new1 - (y1-current_y)
    error2 = m_new2 - (y2-current_y)

    if(error1 + m_new1 > 0):
        x1 +=1
    if(error2 + m_new2 > 0):
        x2 +=1
    return x1,x2

    