
import numpy as np
import graphics_barycentric as cgb
import graphics_classic as cgc
import matplotlib.pyplot as plt
data = np.load("hw1.npy", allow_pickle=True).tolist()
data = dict(data)


verts2d = np.array(data['verts2d'])
vcolors = np.array(data['vcolors'])
faces = np.array(data['faces'])
depth = np.array(data['depth'])
verts2d[:,[1,0]] = verts2d[:,[0,1]]
verts2d = verts2d.astype(int)
img = cgc.render(verts2d, faces, vcolors, depth)

# UNCOMMENT TO RUN BARYCENTRIC IMPLEMENTATION
#img = cgb.render(verts2d, faces, vcolors, depth)


plt.imshow(img)
plt.show()
plt.title("CLASSIC")

