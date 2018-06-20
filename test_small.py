import cv2
from Region import Region
import numpy as np
import GraphCoarse


if __name__ == '__main__':
    image = np.zeros((4,4))
    for r in image.shape[0]:
        for c in image.shape[1]:
            image[r,c] = c*10

    print("Image:",image)

    G0 = GraphCoarse.image_to_graph(image)

    G1 = GraphCoarse.coarse_0(G0)

