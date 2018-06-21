import cv2
from Region import Region
import numpy as np
import GraphCoarse


if __name__ == '__main__':
    image = np.zeros((3,3))
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            image[r,c] = c*10

    print("Image:",image)

    G0 = GraphCoarse.image_to_graph(image)


    G1s = GraphCoarse.coarse_0(G0)

    for g in G1s:
        print(g.T)

