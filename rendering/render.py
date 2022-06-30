import numpy as np
from .shade import shade_phong, shade_gouraud, shade_triangle
from .helpers import rasterize, calculate_normals
from transformations.projection import project_cam_lookat


def render_object(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, face_indices, ka, kd, ks, n,
                  light_positions, light_intensities, Ia):
    """
    Renders an object made of a specific material, placed in a scene with light sources and a camera.
    It calculates how light is reflected onto the object, and its final color at each point.

    :param shader: a variable used to select the function to be used to fill the triangles
    :param focal: the distance of the projection from the centre of the camera measured in the units used by the camera coordinate system
    :param eye: the 3 × 1 vector containing the coordinates of the centre of the camera.
    :param lookat: the 3 × 1 vector containing the coordinates of the camera target point.
    :param up: the 3 × 1 unit "up" vector of the camera.
    :param bg_color: the 3 × 1 vector with the colour components of the background.
    :param M: the height of the generated image in pixels
    :param N: the width of the generated image in pixels
    :param H: the physical height of the camera lens in units of length identical to those used in the camera coordinate system.
    :param W: the physical width of the camera lens in units of length identical to those used in the camera coordinate system.
    :param verts: is a 3 × N matrix with the coordinates of the vertices of the object
    :param vert_colors: a 3 × N matrix with the colour components of each vertex of the object
    :param face_indices: a 3×N matrix describing the triangles
    :param ka: the factor of diffused light from the environment
    :param kd: the diffuse reflection coefficient of the Phong model
    :param ks: the specular reflection coefficient of the Phong model
    :param n: the Phong coefficient
    :param light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
    :param light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).
    :param Ia: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].

    :return: final image with a photographed object
    """
    normals = calculate_normals(verts, face_indices)
    verts_projected, depth = project_cam_lookat(eye, lookat, up, verts, focal)
    verts2d = rasterize(verts_projected, M, N, H, W)
    verts2d = np.array(verts2d).astype(int)
    image_shape = (M, N, 3)
    img = np.ones(image_shape)

    # Average depth of every triangle
    depth_order = np.array(np.mean(depth[face_indices], axis=1))

    # Sort triangles by depth
    sorted_triangles = list(np.flip(np.argsort(depth_order)))

    if shader == 'Gouraud':
        for triangle in sorted_triangles:
            triangle_vertices_indeces = face_indices[triangle]
            triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
            triangle_vcolors = np.array(vert_colors[triangle_vertices_indeces])
            img = shade_triangle(img, triangle_verts2d, triangle_vcolors, 'Gouraud')

    if shader == 'Flat':
        for triangle in sorted_triangles:
            triangle_vertices_indeces = face_indices[triangle]
            triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
            triangle_vcolors = np.array(vert_colors[triangle_vertices_indeces])
            img = shade_triangle(img, triangle_verts2d, triangle_vcolors, 'Flat')

    if shader == 'Phong':
        for triangle in sorted_triangles:
            triangle_vertices_indeces = face_indices[triangle]
            triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
            triangle_vcolors = np.array(vert_colors[triangle_vertices_indeces])
            barycentre_coords = np.mean(verts[triangle_vertices_indeces], axis=0)
            img = shade_phong(triangle_verts2d, normals[triangle_vertices_indeces], triangle_vcolors, barycentre_coords,
                              eye, ka, kd, ks, n,
                              light_positions, light_intensities, Ia, img)
    return img


def render_object_camera(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up):
    """
    Renders an object by projecting it onto the camera lens and then quantizing the image. The color and how the light
    falls on the object are known prior


    :param verts_3d: a Nx3 Matrix containing every point of the object
    :param faces: a Nx3 matrix containing every triangle points
    :param vcolors: a NX3 matrix containing every RGB Color of every vertice
    :param img_h: The height of the image, measured in pixels
    :param img_w: The width of the image, measured in pixels
    :param cam_h: The height of the camera, measured in world units
    :param cam_w: The width of the camera, measured in world units
    :param f: How far is the camera lens from the camera's shutter, measured in world units
    :param c_org: A point indicating where is the camera in the scene of the world
    :param c_lookat: The point where the camera looks/focuses
    :param c_up: A vector indicating the standing side of the camera
    :return: An image with containing a photographed object
    """
    verts_2d, depth = project_cam_lookat(c_org, c_lookat, c_up, verts_3d, f)
    verts_2d = rasterize(verts_2d, img_h, img_w, cam_h, cam_w)
    verts_2d = np.array(verts_2d).astype(int)
    # verts_2d[:, [0, 1]] = verts_2d[:, [1, 0]]
    return render_object(verts_2d, faces, vcolors, depth, "GOURAUD")


def render_object_base(verts2d, faces, vcolors, depth, shade_t="FLAT"):
    """
    Renders an object which has been previously projected onto a camera
    :param verts2d:
    :param faces:
    :param vcolors:
    :param depth:
    :param shade_t:
    :return:
    """
    if shade_t not in ['FLAT', 'GOURAUD']:
        print("Mode not found")
        return
    M = N = 512
    image_shape = (M, N, 3)
    img = np.ones(image_shape)
    # Average depth of every triangle
    depth_order = np.array(np.mean(depth[faces], axis=1))
    # Sort triangles by depth
    sorted_triangles = list(np.flip(np.argsort(depth_order)))
    for triangles in sorted_triangles:
        triangle_vertices_indeces = faces[triangles]
        triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
        triangle_vcolors = np.array(vcolors[triangle_vertices_indeces])
        img = shade_triangle(img, triangle_verts2d, triangle_vcolors, shade_t)
    return img
