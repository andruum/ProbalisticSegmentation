import cv2
from Region import Region
import numpy as np
import GraphCoarse

import random
import sys

SHAPE = (10,10)

import pickle

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
    image = cv2.imread('rsz_1test2.jpg', 0)
    return image

def getTestArray():
    image = np.zeros(SHAPE)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            image[r,c] = 100 if c < SHAPE[0]/2 else 0
    return image

def dumpGraph(Gs):
    sys.setrecursionlimit(1000)
    pickle.dump(Gs, open("save.p", "wb"))
def loadGraph():
    return pickle.load(open("save.p", "rb"))

if __name__ == '__main__':

    image = getImage()
    G0 = GraphCoarse.image_to_graph(image)
    Gs = GraphCoarse.coarse_0(G0)
    #dumpGraph(Gs)



    #Gs = loadGraph()

    while len(Gs)>100:
        Gs = GraphCoarse.coarse(Gs)
        print("Current:",len(Gs))

    #print(len(Gs))
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