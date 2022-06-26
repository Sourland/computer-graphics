import numpy as np
import matplotlib.pyplot as plt
from rendering import nD_rendering as nD
from transformations.transform import affine_transform

data = np.load("../materials/hw2.npy", allow_pickle=True).tolist()
verts_3d = np.array(data['verts3d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
c_org = np.array(data['c_org'])
c_lookat = np.array(data['c_lookat'])
c_up = np.array(data['c_up'])
t_1 = np.array(data['t_1'])
t_2 = np.array(data['t_2'])
u = np.array(data['u'])
phi = np.array(data['phi'])
img_h = img_w = 512
cam_h = cam_w = 15
f = 70

img = nD.render_object(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
plt.imshow(img)
plt.savefig('Image1.jpeg')

verts_3d = affine_transform(verts_3d, u, 0, t_1)
img = nD.render_object(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
plt.imshow(img)
plt.savefig('Image2.jpeg')

verts_3d = affine_transform(verts_3d, u, phi)
img = nD.render_object(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
plt.imshow(img)
plt.savefig('Image3.jpeg')

verts_3d = affine_transform(verts_3d, u, 0, t_2)
img = nD.render_object(verts_3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
plt.imshow(img)
plt.savefig('Image4.jpeg')


