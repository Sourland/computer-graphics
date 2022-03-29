import numpy as np
import graphics as cg

if __name__ == "__main__":
    C1 = np.array([0.1, 0.5, 0.8])
    C2 = np.array([0.8, 0.6, 0.2])
    x1 = 0.5
    x2 = 0.9
    x = 0.7
    print(cg.interpolate_color(x1, x2,x,C1, C2))
