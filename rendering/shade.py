import numpy as np
import transformations.transform as tra
from numpy import linalg as la
from rendering import helpers as h


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

    :return:
    """
    ...


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


def shade_phong(vertsp, vertsn, vertsc, bcoords, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia, X):
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