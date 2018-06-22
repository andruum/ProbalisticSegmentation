import cv2
from Region import Region
import numpy as np
import GraphCoarse

import utils

if __name__ == '__main__':

    image = utils.getImage('rsz_1test2.jpg')

    G0 = GraphCoarse.image_to_graph(image)
    Gs = GraphCoarse.coarse_0(G0)

    while len(Gs)>10:
        Gs = GraphCoarse.coarse(Gs)
        print("Current:",len(Gs))

    utils.debugImage(Gs,image)
