
import numpy as np
import graphics_barycentric as cgb
import graphics_classic as cgc
import matplotlib.pyplot as plt
import helpers as h
data = np.load("hw1.npy", allow_pickle=True).tolist()
data = dict(data)


verts2d = np.array(data['verts2d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
depth = np.array(data['depth'])
verts2d[:,[1,0]] = verts2d[:,[0,1]]
verts2d = verts2d.astype(int)
img = cgc.render(verts2d, faces, vcolors, depth)

# verts2d = np.array([[10,10],[2,30],[2,30]])
# verts2d[:,[1,0]] = verts2d[:,[0,1]]
# print(h.slope(verts2d[0,:], verts2d[1,:]))
# print(h.slope(verts2d[0,:], verts2d[2,:]))
# print(h.slope(verts2d[1,:], verts2d[2,:]))
# print(np.unique(verts2d, axis = 0))
# vcolors = np.array([[0.56, 0.32, 0.18],[0.1, 0.99, 0.7], [0.69, 0.42, 0.05]])
# print(vcolors)
# img = np.ones((35,35,3))
# img = cgc.shade_triangle(img, verts2d, vcolors)



plt.imshow(img)
plt.show()
