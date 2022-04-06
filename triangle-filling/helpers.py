import numpy as np
sorter_bottom = lambda verts2d : np.array([verts2d[0,:],verts2d[1,:],verts2d[2,:]]) if verts2d[1,0] < verts2d[2,0] else np.array([verts2d[0,:],verts2d[2,:],verts2d[1,:]])
sorter_top = lambda verts2d : np.array([verts2d[0,:],verts2d[1,:],verts2d[2,:]]) if verts2d[0,0] < verts2d[1,0] else np.array([verts2d[1,:],verts2d[0,:],verts2d[2,:]])
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
    elif point1[1] == point2[1]:
        return 1/np.inf
    else:
        return (point1[1]-point2[1])/(point1[0]-point2[0])

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
