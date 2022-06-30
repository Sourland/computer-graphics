import numpy as np
import transformations.transform as tra
from numpy import linalg as la
from rendering import helpers as h


def ambient_light(K_a, I_a):
    """
    Calculates the illumination of a point P, which belongs to a surface with a material of type-Phong
    due to diffuse illumination from the environment.

    :param K_a: the factor of diffused light from the environment
    :param I_a: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].
    :return: the trichromatic intensity, reflected from point P. The intensity contributes cumulatively to the colour of the pixel.
    """
    return K_a * I_a.reshape(3,)


def diffuse_light(P, N, color, kd, light_positions, light_intensities):
    """
    Calculates the illumination of a point P due to diffuse reflection

    :param P: a 3x1 vector containing the coordinates of point P.
    :param N: a 3x1 vector with the coordinates of the surface normal vector at point P. The vector has direction towards the outside of the surface, i.e. towards the observer's side.
    :param color: a 3×1 vector with the colour components of point P. Each component belongs to the interval [0, 1].
    :param kd: the diffuse reflection coefficient of the Phong model
    :param light_positions: a list of 3 × 1 vectors containing the components of the position of the light sources.
    :param light_intensities: a list of 3 × 1 vectors containing the intensities of the bright sources (corresponding to light_positions).
    :return: the trichromatic intensity, reflected from point P. The intensity contributes cumulatively to the final colour of the pixel.
    """

    L = (P - light_positions) / la.norm(P - light_positions)
    angle = np.dot(L, N.reshape((3, 1)))
    I_lambda = (light_intensities * kd * angle)
    return np.multiply(color, I_lambda).reshape(3,)


def specular_light(P, N, color, cam_pos, ks, n, light_positions, light_intensities):
    """
    Calculates the illumination of a point P due to specular reflection

    :param P: a 3 × 1 column vector with the coordinates of point P
    :param N: is a 3 × 1 column vector with the coordinates of the normal vector of the surface at point P (i.e. the vector perpendicular to the surface). The vector has direction towards the outside of the surface, i.e. towards the side of the observer.
    :param color: the 3×1 vector with the colour components of point P. Each component belongs to the interval [0, 1].
    :param cam_pos: a 3 × 1 column vector with the coordinates of the observer (i.e. the camera)
    :param ks: the specular reflection coefficient of the Phong model
    :param n: the Phong coefficient
    :param light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
    :param light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).
    :return: the intensity of trichromatic radiation reflected from point P. The intensity contributes cumulatively to the colour of the pixel.
    """

    V = (cam_pos - P) / la.norm((cam_pos - P))
    L = (P - light_positions) / la.norm(P - light_positions)
    LN_inner_product = np.dot(N.T, L.T)
    angle = np.dot(2 * N.T * LN_inner_product - L, V) ** n
    I_lambda = light_intensities * ks * angle
    return np.multiply(color, I_lambda).reshape(3,)
