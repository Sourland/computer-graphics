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

    t = (x-x1)/(x2-x1) #slope of linear interpolation
    C = np.zeros(3) #Initialize the C color vector
    #Calculating colors at x
    C[0] = abs(C1[0]) + t*(C2[0]-C1[0]) 
    C[1] = abs(C1[1]) + t*(C2[1]-C1[1])
    C[2] = abs(C1[2]) + t*(C2[2]-C1[2])
    return C

def shade_triangle(img, verts2d, vcolors, shade_t = 'flat'):
    print('lol')
