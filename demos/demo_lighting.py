import numpy as np
from rendering.shade import render_object
import matplotlib.pyplot as plt

data = np.load("../materials/hw3.npy", allow_pickle=True).tolist()

verts = np.array(data['verts'])
vertex_colors = np.array(data['vertex_colors'])
face_indices = np.array(data['face_indices'])
depth = np.array(data['depth'])
cam_eye = np.array(data['cam_eye'])
cam_up = np.array(data['cam_up'])
cam_lookat = np.array(data['cam_lookat'])
ka = np.array(data['ka'])
kd = np.array(data['kd'])
ks = np.array(data['ks'])
n = np.array(data['n'])
light_positions = np.array(data['light_positions'])
light_intensities = np.array(data['light_intensities'])
Ia = np.array(data['Ia'])
M = np.array(data['M'])
N = np.array(data['N'])
W = np.array(data['W'])
H = np.array(data['H'])
bg_color = np.array(data['bg_color'])
focal = 70

img = render_object('Phong', focal, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vertex_colors,
                    face_indices, ka, kd, ks, n, light_positions, light_intensities, Ia)

plt.imshow(img)
plt.show()
plt.title("CLASSIC")
