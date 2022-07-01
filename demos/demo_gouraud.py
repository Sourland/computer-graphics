import numpy as np
from rendering.render import render_object_base
import matplotlib.pyplot as plt


data = np.load("../materials/hw1.npy", allow_pickle=True).tolist()
data = dict(data)

verts2d = np.array(data['verts2d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
depth = np.array(data['depth'])
verts2d[:,[1,0]] = verts2d[:,[0,1]]
verts2d = verts2d.astype(int)

img = render_object_base(verts2d, faces, vcolors, depth, 'Gouraud')

plt.savefig('../results/Assignment 1 - Triangle Filling/Image_Fish_Gouraud.jpeg')
plt.imshow(img)
plt.show()
