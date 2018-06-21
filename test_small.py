import cv2
from Region import Region
import numpy as np
import GraphCoarse

import random

SHAPE = (10,10)

def debug_region(reg,image,Gid):
    if reg.pixel:
        row = int(reg.id / SHAPE[1])
        col = reg.id - row * SHAPE[1]
        image[row, col] = Gid
    else:
        for sr in reg.subregions:
            debug_region(sr,image,Gid)

def debug(region):
    image = np.zeros(SHAPE)
    for reg in region:
        debug_region(reg,image,reg.id)
    print(image)

def getImage():
    image = cv2.imread('test2.jpg', 0)
    return image

def getTestArray():
    image = np.zeros(SHAPE)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            image[r,c] = 100 if c < SHAPE[0]/2 else 0
    return image

if __name__ == '__main__':

    image = getImage()

    G0 = GraphCoarse.image_to_graph(image)

    Gs = GraphCoarse.coarse_0(G0)

    #debug(Gs)
    len(Gs)

    Gs = GraphCoarse.coarse(Gs)

    #debug(Gs)
    #
    # if len(Gs) != 2:
    #     complete = False
    #     while complete == False:
    #         Gs = GraphCoarse.coarse(Gs)
    #         if len(Gs) <= 2:
    #             complete = True
    #
    #
    # print(len(Gs))