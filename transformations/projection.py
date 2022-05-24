import numpy
import numpy as np
import transformations.transform as tra
from numpy import linalg as la
from rendering import helpers as h


def project_cam(c_v, c_x, c_y, c_z, p, f=1):
    """
    Simulation of a real-world camera. Applies projection of point p to the camera lens
    Args:
        f: The distance between the camera lens and the inside camera shutter
        c_v: The coordinates of the camera displacement vector expressed in the WCS
        c_x: The coordinates of the camera x vector expressed in the WCS
        c_y: The coordinates of the camera y vector expressed in the WCS
        c_z: The coordinates of the camera z vector expressed in the WCS
        p: The coordinates of N triangle vertices points to apply the projection, expressed in the WCS

    Returns:
        verts2d: The coordinates of N projected triangle vertices points to apply the projection, expressed in the WCS
        depth: Every depth of the projected triangle vertices points
    """
    c_v, c_x, c_y, c_z, p = h.casting(c_v, c_x, c_y, c_z, p)
    R = np.vstack((c_x, c_y, c_z)).T
    p = tra.system_transform(p, R, c_v)
    depth = p[:, 2]
    x_projected = (f / depth) * p[:, 1]
    y_projected = (f / depth) * p[:, 0]
    verts2d = np.vstack((x_projected, y_projected))

    return verts2d.T, depth


def project_cam_lookat(c_org, c_lookat, c_up, verts_3d, f=1):
    """
    Points a camera to a certain point and applies projection of point p to the camera lens
    Args:
        c_org: The position of the camera in a scene
        c_lookat: The point where the camera looks/focuses
        c_up: A vector indicating the standing side of the camera
        verts_3d: The points of an object
        f: The distance between the camera lens and the inside camera shutter
    Returns:

    """
    c_lookat = np.array(c_lookat) + np.array(c_org)
    c_z = c_lookat / la.norm(c_lookat)
    t = np.array(c_up - np.dot(c_up, c_z) * c_z)
    c_y = t / la.norm(t)
    c_x = numpy.cross(c_y, c_z)
    c_x, c_y, c_z = h.casting(c_x, c_y, c_z)
    return project_cam(c_org, c_x, c_y, c_z, verts_3d, f)


