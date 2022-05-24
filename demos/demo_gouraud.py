import numpy as np
import rendering.scanline_rendering as scanline
import rendering.simplex_rendering as simplex
import matplotlib.pyplot as plt
data = np.load("../rendering/hw1.npy", allow_pickle=True).tolist()
data = dict(data)


verts2d = np.array(data['verts2d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
depth = np.array(data['depth'])
verts2d[:,[1,0]] = verts2d[:,[0,1]]
verts2d = verts2d.astype(int)

img = scanline.render(verts2d, faces, vcolors, depth, 'GOURAUD')

# UNCOMMENT TO RUN BARYCENTRIC IMPLEMENTATION
#img = simplex.render(verts2d, faces, vcolors, depth, 'GOURAUD')

plt.imshow(img)
plt.show()
