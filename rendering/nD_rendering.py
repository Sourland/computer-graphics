import numpy as np
from rendering import scanline_rendering as scanline
import transformations.projection as pro


def rasterize(verts_2d, img_h, img_w, cam_h, cam_w):
    """
    Takes every projected point from the camera's shutter and places them in a digital photo.
    Args:
        verts_2d: a Nx3 matrix containing every projected point
        img_h: The height of the image, measured in pixels
        img_w: The width of the image, measured in pixels
        cam_h: The height of the camera, measured in world units
        cam_w: The width of the camera, measured in world units

    Returns:
        verts_rast: projected points placed in a canvas
    """

    verts_rast = np.zeros((len(verts_2d), 2))
    width = img_w / cam_w
    height = img_h / cam_h
    for i in range(len(verts_2d)):
        verts_rast[i, 0] = np.around((verts_2d[i, 0] + cam_h / 2) * height - 0.5)
        verts_rast[i, 1] = np.around((-verts_2d[i, 1] + cam_w / 2) * width - 0.5)

    return verts_rast


def render_object(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up):
    """
    Projects an object from a scene to the image lens and then rasterized the image to create a photograph of the object
    Args:
        verts_3d: a Nx3 Matrix containing every point of the object
        faces: a Nx3 matrix containing every triangle points
        vcolors: a NX3 matrix containing every RGB Color of every vertice
        img_h: The height of the image, measured in pixels
        img_w: The width of the image, measured in pixels
        cam_h: The height of the camera, measured in world units
        cam_w: The width of the camera, measured in world units
        f: How far is the camera lens from the camera's shutter, measured in world units
        c_org: A point indicating where is the camera in the scene of the world
        c_lookat: The point where the camera looks/focuses
        c_up: A vector indicating the standing side of the camera

    Returns:
        An image with containing a photographed object
    """
    verts_2d, depth = pro.project_cam_lookat(c_org, c_lookat, c_up, verts_3d, f)
    verts_2d = rasterize(verts_2d, img_h, img_w, cam_h, cam_w)
    verts_2d = np.array(verts_2d).astype(int)
    # verts_2d[:, [0, 1]] = verts_2d[:, [1, 0]]
    return scanline.render(verts_2d, faces, vcolors, depth, "GOURAUD")
