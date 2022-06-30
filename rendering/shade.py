import numpy as np
import math
from rendering.helpers import calculate_normals, rasterize, update_active_edges, find_initial_elements, slope, \
    interpolate_color, interpolate_vector
from rendering.scanline_rendering import Edge, shade_triangle
from rendering.light import ambient_light, diffuse_light, specular_light
from transformations.projection import project_cam_lookat


def render_object(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, face_indices, ka, kd, ks, n,
                  light_positions, light_intensities, Ia):
    """
    Creates the color photo image of a 3D object, calculating the color based on the materials models

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
    for i in range(len(vert_colors)):
        vert_colors[i] = ambient_light(ka, Ia) + \
                         diffuse_light(verts[i], normals[i], vert_colors[i], kd, light_positions, light_intensities) + \
                         specular_light(verts[i], normals[i], vert_colors[i], eye, ks, n, light_positions,
                                        light_intensities)

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
            img = shade_phong(triangle_verts2d, normals[triangle_vertices_indeces], triangle_vcolors, barycentre_coords, eye, ka, kd, ks, n,
                              light_positions, light_intensities, Ia, img)
    return img


def shade_gouraud(vertsp, vertsn, vertsc, bcoords, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia, X):
    """

    :param vertsp: a 2 × 3 matrix containing the coordinates of the vertices of the triangle after they have been projected onto the camera screen.
    :param vertsn: a 3 × 3 matrix containing in its columns the normal vectors of the vertices of the triangle.
    :param vertsc: a 3 × 3 matrix containing the colour components for each point of the triangle.
    :param bcoords: a vector of dimension 3×1 contains the centre of gravity of the triangle before its projection.
    :param cam_pos: a 3 × 1 column vector with the coordinates of the observer (i.e. the camera).
    :param ka: the factor of diffused light from the environment
    :param kd: the diffuse reflection coefficient of the Phong model
    :param ks: the specular reflection coefficient of the Phong model
    :param n: the Phong coefficient
    :param light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
    :param light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).
    :param Ia: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].
    :param X: an image (M × N × 3 matrix) with any pre-existing triangles
    :return: the final image with rendered triangles
    """

    ...


def shade_phong(vertice_positions, vertice_normal_vectors, vertice_colors, barycentre_coords, cam_pos, ka, kd, ks, n,
                light_positions, light_intensities, Ia, img):
    """

    :param vertice_positions: a 2 × 3 matrix containing the coordinates of the vertices of the triangle after they have been projected onto the camera screen.
    :param vertice_normal_vectors: a 3 × 3 matrix containing in its columns the normal vectors of the vertices of the triangle.
    :param vertice_colors: a 3 × 3 matrix containing the colour components for each point of the triangle.
    :param barycentre_coords: a vector of dimension 3×1 contains the barycentre of the triangle before its projection.
    :param cam_pos: a 3 × 1 column vector with the coordinates of the observer (i.e. the camera).
    :param ka: the factor of diffused light from the environment
    :param kd: the diffuse reflection coefficient of the Phong model
    :param ks: the specular reflection coefficient of the Phong model
    :param n: the Phong coefficient
    :param light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
    :param light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).
    :param Ia: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].
    :param img: an image (M × N × 3 matrix) with any pre-existing triangles
    :return: the final image with rendered triangles
    """

    # if np.all(vertice_positions[0, 0] == vertice_positions[:, 0]) and \
    #         np.all(vertice_positions[:, 1] == vertice_positions[0, 1]):
    #     return img
    #
    # if len(np.unique(vertice_positions, axis=0)) < 3:
    #     return img

    # Initialize Edge elements
    Edge1 = Edge("AB", np.array([vertice_positions[0, :], vertice_positions[1, :]]),
                 np.array([vertice_colors[0, :], vertice_colors[1, :]]),
                 slope(vertice_positions[0, :], vertice_positions[1, :]), False)
    Edge2 = Edge("BC", np.array([vertice_positions[1, :], vertice_positions[2, :]]),
                 np.array([vertice_colors[1, :], vertice_colors[2, :]]),
                 slope(vertice_positions[1, :], vertice_positions[2, :]), False)
    Edge3 = Edge("AC", np.array([vertice_positions[0, :], vertice_positions[2, :]]),
                 np.array([vertice_colors[0, :], vertice_colors[2, :]]),
                 slope(vertice_positions[0, :], vertice_positions[2, :]), False)

    Edge1.set_normal_vectors(np.array([vertice_normal_vectors[0], vertice_normal_vectors[1]]))
    Edge2.set_normal_vectors(np.array([vertice_normal_vectors[1], vertice_normal_vectors[2]]))
    Edge3.set_normal_vectors(np.array([vertice_normal_vectors[0], vertice_normal_vectors[2]]))

    # Define minimum and maximum y
    y_max = np.array(np.max(vertice_positions, axis=0))[1]
    y_min = np.array(np.min(vertice_positions, axis=0))[1]

    # Initialize search parameters
    edges = [Edge1, Edge2, Edge3]
    active_edges = []
    horizontal_line = False
    # Begin search for initial elements
    for i in range(len(edges)):
        if y_min == edges[i].y_min:
            if edges[i].slope != 0:
                edges[i].is_active = True
                active_edges.append(i)
            else:
                horizontal_line = True

    # Act based on active edge findings
    if len(active_edges) < 2:
        return img
    if not horizontal_line:
        for i in range(len(vertice_positions)):
            if vertice_positions[i, 1] == y_min:
                index = i
                x1 = vertice_positions[i, 0]
                x2 = x1
        if 0 <= x1 <= img.shape[0] - 1 and 0 <= y_min <= img.shape[1] - 1:
            img[int(math.floor(x1 + 0.5)), int(math.floor(y_min + 0.5))] = vertice_colors[index, :]
    else:
        x1, x2, C1, C2, n1, n2 = find_initial_elements(edges, active_edges)
        for x in range(x1, x2 + 1):
            if 0 <= x <= img.shape[0] - 1 and 0 <= y_min <= img.shape[1] - 1:
                color = interpolate_color(x1, x2, x, C1, C2)
                normal_vector = interpolate_vector(x1, x2, x, vertice_normal_vectors[n1], vertice_normal_vectors[n2])
                img[x, y_min] = ambient_light(ka, Ia) + \
                                diffuse_light(barycentre_coords, normal_vector, color, kd, light_positions,
                                              light_intensities) + \
                                specular_light(barycentre_coords, normal_vector, color, cam_pos, ks, n, light_positions,
                                               light_intensities)

    # Begin Scanline Algorithm
    for y in range(y_min + 1, y_max + 1):
        if edges[active_edges[0]].slope != float('inf'):
            x1 = x1 + 1 / edges[active_edges[0]].slope
        if edges[active_edges[1]].slope != float('inf'):
            x2 = x2 + 1 / edges[active_edges[1]].slope

        color_A = interpolate_color(edges[active_edges[0]].y_min, edges[active_edges[0]].y_max, y,
                                    edges[active_edges[0]].colors[0, :], edges[active_edges[0]].colors[1, :])
        normal_vector_1 = interpolate_vector(edges[active_edges[0]].y_min, edges[active_edges[0]].y_max, y,
                                             edges[active_edges[0]].normal_vectors[0, :],
                                             edges[active_edges[0]].normal_vectors[1, :])

        color_B = interpolate_color(edges[active_edges[1]].y_min, edges[active_edges[1]].y_max, y,
                                    edges[active_edges[1]].colors[0, :], edges[active_edges[1]].colors[1, :])
        normal_vector_2 = interpolate_vector(edges[active_edges[1]].y_min, edges[active_edges[1]].y_max, y,
                                             edges[active_edges[1]].normal_vectors[0, :],
                                             edges[active_edges[1]].normal_vectors[1, :])

        for x in range(int(min(x1, x2)), int(max(x1, x2)) + 1):
            if 0 <= x <= img.shape[0] - 1 and 0 <= y <= img.shape[1] - 1:
                color = interpolate_color(int(x1), int(x2), int(math.floor(x + 0.5)),
                                          color_A, color_B)
                normal_vector = interpolate_vector(x1, x2, x, normal_vector_1, normal_vector_2)
                img[int(math.floor(x + 0.5)), y] = ambient_light(ka, Ia) + \
                                diffuse_light(barycentre_coords, normal_vector, color, kd, light_positions,
                                              light_intensities) + \
                                specular_light(barycentre_coords, normal_vector, color, cam_pos, ks, n, light_positions,
                                               light_intensities)
        active_edges = update_active_edges(edges, active_edges, y)
    return img
