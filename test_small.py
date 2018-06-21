import cv2
from Region import Region
import numpy as np
import GraphCoarse

import random

SHAPE = (20,20)

def debug_region(region):
    image = np.zeros(SHAPE)
    for g in region:
        for s in g.subregions:
            r = int(s.id / SHAPE[1])
            c = s.id - r * SHAPE[1]
            image[r,c] = g.id
    print(image)

if __name__ == '__main__':
    image = np.zeros(SHAPE)
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            image[r,c] = 100 if c < 5 else 0

    print("Image:",image)

    G0 = GraphCoarse.image_to_graph(image)

    G1s = GraphCoarse.coarse_0(G0)

    debug_region(G1s)

    # complete = False
    # Gsd = G1s
    # while complete == False:
    #     Gs = GraphCoarse.coarse(Gsd)
    #     if len(Gs) == len(Gsd):
    #         complete = True
    #     else:
    #         Gsd = Gs
    #
    # print(len(Gsd))