import numpy as np
sorter_bottom = lambda verts2d : np.array([verts2d[0,:],verts2d[1,:],verts2d[2,:]]) if verts2d[1,0] < verts2d[2,0] else np.array([verts2d[0,:],verts2d[2,:],verts2d[1,:]])
sorter_top = lambda verts2d : np.array([verts2d[0,:],verts2d[1,:],verts2d[2,:]]) if verts2d[0,0] < verts2d[1,0] else np.array([verts2d[1,:],verts2d[0,:],verts2d[2,:]])

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