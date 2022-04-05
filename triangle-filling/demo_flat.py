from re import A
import numpy as np
import graphics as cg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
data = np.load("hw1.npy", allow_pickle=True).tolist()
data = dict(data)


verts2d = np.array(data['verts2d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
depth = np.array(data['depth'])
verts2d[:,[1,0]] = verts2d[:,[0,1]]
verts2d = verts2d.astype(int)
verts2d = np.array([[2,2], [2, 30], [15, 20]])
vcolors = np.array([[0.56, 0.32, 0.18],[0.1, 0.99, 0.7], [0.69, 0.42, 0.05]])
img = np.ones((35,35,3))
img = cg.shade_triangle(img, verts2d, vcolors)

#img = cg.render(verts2d, faces, vcolors, depth, "FLAT")

print(img)
plt.imshow(img)
plt.show()
