import numpy as np
from numpy import linalg as la


def affine_transform(c_p, u, theta=0, t=3 * [0]):
    """
    Perform an affine transformation to a point expressed in a coordinate system. This function can apply displacement
    and rotation
    Args:
        c_p: 3xN matrix containing the coordinates of N points expressed in a coordinate system
        theta: angle of rotation
        u: 3x1 rotation axis vector
        t: 3x1 displacement vector

    Returns:
        c_q: Nx3 matrix containing the transformed coordinates of N points expressed in a coordinate system
        theta: angle of rotation
    """
    u = np.array(u) / la.norm(u)
    if c_p.ndim > 1:
        c_p = np.hstack((c_p, np.ones((c_p.shape[0], 1))))
    else:
        c_p = np.append(c_p, 1)
    T_h = np.eye(4)
    T_h[0:3, 3] = np.array(t)
    row_1 = np.array([(1 - np.cos(theta)) * u[0] ** 2 + np.cos(theta),
                      (1 - np.cos(theta)) * u[0] * u[1] - np.sin(theta) * u[2],
                      (1 - np.cos(theta)) * u[0] * u[2] + np.sin(theta) * u[1]])
    row_2 = np.array([row_1[1],
                      (1 - np.cos(theta)) * u[1] ** 2 + np.cos(theta),
                      (1 - np.cos(theta)) * u[1] * u[2] - np.sin(theta) * u[0]])
    row_3 = np.array([row_1[2], row_2[2], (1 - np.cos(theta)) * u[2] ** 2 + np.cos(theta)])
    T_h[0:3, 0:3] = np.vstack((row_1, row_2, row_3))

    c_q = np.dot(T_h, c_p.T).T
    if c_q.ndim > 1:
        c_q = np.delete(c_q, 3, 1)
    else:
        c_q = np.array(c_q[0:3])
    return c_q


def system_transform(c_p, R, c_0):
    """
    Find the coordinates of c_p expressed in a different coordinate system. The relationship between the old and the
    new coordinate system is defined by a rotation angle, a rotation axis and an offset vector vp
    Args:
        c_p: 3xN matrix containing the coordinates of N points expressed in a coordinate system
        R:
        c_0: 3x1 coordinate system offset rotation axis vector

    Returns:
        d_p: a Nx3 matrix containing the coordinates of N points expressed in a different coordinate system
    """

    if c_p.ndim == 1:
        c_p = (c_p - c_0)
    else:
        c_p = np.array([c_p[i, :] - c_0 for i in range(c_p.shape[0])])
    return np.dot(R, c_p.T).T
