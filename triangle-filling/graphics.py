import numpy as np
import helpers as hp
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



def fill_bottom_triangle(img, verts2d, vcolors, shade_t='FLAT'):
    """Colors a triangle that has a flat edge at the bottom
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
        An image with said triangle fully colored
    """
    verts2d = verts2d[verts2d[:, 1].argsort()[::-1]]
    verts2d = hp.sorter(verts2d)
    slope1 = hp.slope(verts2d[1,:],verts2d[0,:]) 
    slope2 = hp.slope(verts2d[2,:],verts2d[0,:]) 
    x1 = verts2d[0,0]
    x2 = x1
    if shade_t == 'FLAT':
        flat_color = np.mean(vcolors, axis = 1)
        img[verts2d[0,1],x1,0] = flat_color[0]
        img[verts2d[0,1],x1,1] = flat_color[1]
        img[verts2d[0,1],x1,2] = flat_color[2]
        for y in range(verts2d[0,1], verts2d[1,1]+1):
            for x in range(x1,x2):
                img[y,x,0] = flat_color[0]
                img[y,x,1] = flat_color[1]
                img[y,x,2] = flat_color[2]
            if x1 == x2 and x1 != verts2d[0,0]:
                img[y,x1,0] = flat_color[0]
                img[y,x1,1] = flat_color[1]
                img[y,x1,2] = flat_color[2]
            x1 = round(x1 + 1/slope1)
            x2 = round(x2 + 1/slope2)
        return img

    elif shade_t == 'GOURAUD':
        for y in range(verts2d[0,1], verts2d[1,1]+1):
            color_A = interpolate_color(verts2d[0,1], verts2d[1,1], y, vcolors[0,:], vcolors[1,:])
            color_B = interpolate_color(verts2d[0,1], verts2d[2,1], y, vcolors[0,:], vcolors[2,:])
            for x in range(x1,x2):
                pixel_color = interpolate_color(x1, x2, x, color_A, color_B)
                img[y,x,0] = pixel_color[0]
                img[y,x,1] = pixel_color[1]
                img[y,x,2] = pixel_color[2]
            x1 = round(x1 + 1/slope1)
            x2 = round(x2 + 1/slope2)
        return img

def fill_top_triangle(img, verts2d, vcolors, shade_t='FLAT'):
    """Colors a triangle that has a flat edge at the top
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
        An image with said triangle fully colored
    """
    verts2d = verts2d[verts2d[:, 1].argsort()[::-1]]
    verts2d = hp.sorter(verts2d)
    slope1 = hp.slope(verts2d[1,:],verts2d[0,:]) 
    slope2 = hp.slope(verts2d[2,:],verts2d[0,:]) 
    x1 = verts2d[2,0]
    x2 = x1
    
    if shade_t == 'FLAT':
        Color = np.mean(vcolors, axis = 1)
        for y in range(verts2d[0,1], verts2d[1,1]-1, -1):
            for x in range(x1,x2):
                img[y,x,:] = Color
            x1 = round(x1 + 1/slope1)
            x2 = round(x2+1/slope2)
        return img

    elif shade_t == 'GOURAUD':
        for y in range(verts2d[0,1], verts2d[1,1]):
            color_A = interpolate_color(verts2d[0,1], verts2d[1,1], y, vcolors[0,:], vcolors[1,:])
            color_B = interpolate_color(verts2d[0,1], verts2d[2,1], y, vcolors[0,:], vcolors[2,:])
            for x in range(x1,x2):
                pixel_color = interpolate_color(x1, x2, x, color_A, color_B)
                img[y,x,:] = pixel_color
            x1 = round(x1 + 1/slope1)
            x2 = round(x2+1/slope2)
        return img

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
        ...
    elif shade_t == 'Gouraud':
        ...




    # elif shade_t == 'GOURAUD':
    #     raise NotImplemented
