import cv2
from Region import Region
import numpy as np
import GraphCoarse

import utils

if __name__ == '__main__':

    image = utils.getImage('datasets/rsz_test_keyboard.jpg')

    G0 = GraphCoarse.image_to_graph(image)
    Gs = GraphCoarse.coarse_0(G0)

    while len(Gs)>=5:
        Gs = GraphCoarse.coarse(Gs)
        print("Current:",len(Gs))

    utils.debugImagePixels(Gs,image)
