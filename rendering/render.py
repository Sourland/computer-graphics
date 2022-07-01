import numpy as np
from .shade import shade_phong, shade_gouraud, shade_triangle
from .helpers import rasterize, calculate_normals
from transformations.projection import project_cam_lookat


def render_object(lighting, shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, face_indices, ka,
                  kd, ks, n, light_positions, light_intensities, Ia):
    """
    Renders an object made of a specific material, placed in a scene with light sources and a camera.
    It calculates how light is reflected onto the object, and its final color at each point.

    Args:
        lighting:
        shader: a variable used to select the function to be used to fill the triangles
        focal: the distance of the projection from the centre of the camera measured in the units used by the camera coordinate system
        eye: the 3 × 1 vector containing the coordinates of the centre of the camera.
        lookat: the 3 × 1 vector containing the coordinates of the camera target point.
        up: the 3 × 1 unit "up" vector of the camera.
        bg_color: the 3 × 1 vector with the colour components of the background.
        M: the height of the generated image in pixels
        N: the width of the generated image in pixels
        H: the physical height of the camera lens in units of length identical to those used in the camera coordinate system.
        W: the physical width of the camera lens in units of length identical to those used in the camera coordinate system.
        verts: is a 3 × N matrix with the coordinates of the vertices of the object
        vert_colors: a 3 × N matrix with the colour components of each vertex of the object
        face_indices: a 3×N matrix describing the triangles
        ka: the factor of diffused light from the environment
        kd: the diffuse reflection coefficient of the Phong model
        ks: the specular reflection coefficient of the Phong model
        n: the Phong coefficient
        light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
        light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).
        Ia: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].

    Returns:
        An image with a rendered object
    """
    assert lighting in ['Ambient', 'Diffuse', 'Specular', 'All']
    assert shader in ['Gouraud', 'Phong']

    normals = calculate_normals(verts, face_indices)
    verts_projected, depth = project_cam_lookat(eye, lookat, up, verts, focal)
    verts2d = rasterize(verts_projected, M, N, H, W).astype(int)
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
            barycentre_coords = np.mean(verts[triangle_vertices_indeces], axis=0)
            img = shade_gouraud(lighting, triangle_verts2d, normals[triangle_vertices_indeces], triangle_vcolors,
                                barycentre_coords, eye, ka, kd, ks, n, light_positions, light_intensities, Ia, img)

    if shader == 'Phong':
        for triangle in sorted_triangles:
            triangle_vertices_indeces = face_indices[triangle]
            triangle_verts2d = np.array(verts2d[triangle_vertices_indeces])
            triangle_vcolors = np.array(vert_colors[triangle_vertices_indeces])
            barycentre_coords = np.mean(verts[triangle_vertices_indeces], axis=0)
            img = shade_phong(lighting, triangle_verts2d, normals[triangle_vertices_indeces], triangle_vcolors,
                              barycentre_coords, eye, ka, kd, ks, n, light_positions, light_intensities, Ia, img)
    return img


def render_object_camera(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up):
    """
    Renders an object by projecting it onto the camera lens and then quantizing the image. The color and how the light
    falls on the object are known prior

    Args:
        verts_3d: a Nx3 Matrix containing every triangle vertice of the object
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
        An image with a rendered object
    """
    verts_2d, depth = project_cam_lookat(c_org, c_lookat, c_up, verts_3d, f)
    verts_2d = rasterize(verts_2d, img_h, img_w, cam_h, cam_w).astype(int)

    return render_object_base(verts_2d, faces, vcolors, depth, "Gouraud")


def render_object_base(verts2d, faces, vcolors, depth, shade_t="Flat"):
    """
    Renders an object which has been previously projected onto a camera

    Args:
        verts2d: A N x 3 matrix containing every triangle vertice of a projected object
        faces: A N x 3 list containing the vertices of each triangle
        vcolors: A N x 3 list containing the colors of each vertice
        depth: a N x 1 list containing the depth of each triangle in a scene
        shade_t: the Shading mode. This can be flat(mean of color) or Gouraud(linear interpolation of color)

    Returns:
        An image with a rendered object
    """
    assert shade_t in ['Flat', 'Gouraud']

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
