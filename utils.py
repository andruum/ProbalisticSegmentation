
import cv2
import numpy as np

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

def getImage(imgpath):
    image = cv2.imread(imgpath, 0)
    return image

def getTestArray(rows,cols):
    image = np.zeros((rows,cols))

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            image[r,c] = 100 if c < SHAPE[0]/2 else 0
    return image


def debugImage(Gs,image):
    image_debug = np.zeros(image.shape)

    for g in Gs:
        bp = g.getBoundaryPixels()
        for p in bp:
            r = int(p.id / image.shape[1])
            c = p.id - r * image.shape[1]
            image_debug[r,c] = 255
    showImage(image_debug)

def showImage(img):
    cv2.imshow("debug:", img)
    cv2.waitKey(0)