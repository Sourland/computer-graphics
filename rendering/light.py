import numpy as np
from numpy import linalg as la


def ambient_light(K_a, I_a):
    """
    Calculates the illumination of a point P, which belongs to a surface with a material of type-Phong
    due to diffuse illumination from the environment.

    Args:
        K_a: the factor of diffused light from the environment
        I_a: the 3 × 1 vector with the components of the diffuse irradiance of the ambient radiation intensity. Each component belongs to the interval [0, 1].

    Returns:
        the trichromatic intensity, reflected from point P. The intensity contributes cumulatively to the colour of the pixel.
    """
    return K_a * I_a.reshape(3,)


def diffuse_light(P, N, color, kd, light_positions, light_intensities):
    """
    Calculates the illumination of a point P due to diffuse reflection

    Args:
        P: a 3x1 vector containing the coordinates of point P.
        N: a 3x1 vector with the coordinates of the surface normal vector at point P. The vector has direction towards the outside of the surface, i.e. towards the observer's side.
        color: a 3×1 vector with the colour components of point P. Each component belongs to the interval [0, 1].
        kd: the diffuse reflection coefficient of the Phong model
        light_positions: a list of 3 × 1 vectors containing the components of the position of the light sources.
        light_intensities: a list of 3 × 1 vectors containing the intensities of the bright sources (corresponding to light_positions).

    Returns:
        The trichromatic intensity, reflected from point P. The intensity contributes cumulatively to the final colour of the pixel.
    """

    L = (P - light_positions) / la.norm(P - light_positions)
    angle = np.dot(L, N.reshape((3, 1)))
    I_lambda = (light_intensities * kd * angle)
    return np.multiply(color, I_lambda).reshape(3,)


def specular_light(P, N, color, cam_pos, ks, n, light_positions, light_intensities):
    """
    Calculates the illumination of a point P due to specular reflection

    Args:
        P: a 3 × 1 column vector with the coordinates of point P
        N: is a 3 × 1 column vector with the coordinates of the normal vector of the surface at point P (i.e. the vector perpendicular to the surface). The vector has direction towards the outside of the surface, i.e. towards the side of the observer.
        color: the 3×1 vector with the colour components of point P. Each component belongs to the interval [0, 1].
        cam_pos: a 3 × 1 column vector with the coordinates of the observer (i.e. the camera)
        ks: the specular reflection coefficient of the Phong model
        n: the Phong coefficient
        light_positions: a list of 3 × N vectors containing the components of the position of the light sources.
        light_intensities: a list of 3 × N vectors containing the intensities of the bright sources (corresponding to light_positions).

    Returns:
        The intensity of trichromatic radiation reflected from point P. The intensity contributes cumulatively to the colour of the pixel.
    """

    V = (cam_pos - P) / la.norm((cam_pos - P))
    L = (light_positions - P) / la.norm(light_positions - P)
    LN_inner_product = np.dot(N.T, L.T)
    angle = np.dot(2 * N.T * LN_inner_product - L, V) ** n
    I_lambda = light_intensities * ks * angle
    return np.multiply(color, I_lambda).reshape(3,)
