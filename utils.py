import cv2
import numpy as np
import math
import os
import time

# SHAPEIMG = (100,200)
# SHAPEIMG_SHOW = (SHAPEIMG[0]*4,SHAPEIMG[1]*4)

PIXELS = 20000

def getShapeForCalc(image_shape):
    img_pixels = image_shape[0]*image_shape[1]
    scale = math.sqrt(PIXELS)/math.sqrt(img_pixels)
    return (int(image_shape[0]*scale),int(image_shape[1]*scale))

def getShapeForDebug(image_shape):
    img_pixels = image_shape[0] * image_shape[1]
    if img_pixels<PIXELS:
        return image_shape

    scale = math.sqrt(PIXELS)/math.sqrt(img_pixels)
    scale*=4
    return (int(image_shape[0] * scale), int(image_shape[1] * scale))


def getImage(imgpath):
    image = cv2.imread(imgpath, 0)
    return image

def resizeImg(image):
    return cv2.resize(image, dsize=(getShapeForCalc(image.shape)[1],getShapeForCalc(image.shape)[0]), interpolation=cv2.INTER_NEAREST)

def debugImagePixels(Gs,image):
    print("Found regions:",len(Gs))
    shape = getShapeForCalc(image.shape)

    timev = time.time()
    timev = int(timev)
    path = './results/' + str(timev)
    print('Save to :', path)
    if not os.path.exists(path):
        os.makedirs(path)

    for g in Gs:
        image_debug = np.zeros(shape)
        bp = g.getPixelsRegions()
        for p in bp:
            r = int(p.id / shape[1])
            c = p.id - r * shape[1]
            image_debug[r,c] = 255
        # showImage(image_debug,0)
        saveImage(image_debug,path,g.id)


def showImage(img,time=0, name = 'debug'):
    img_res = cv2.resize(img, dsize=(getShapeForDebug(img.shape)[1], getShapeForDebug(img.shape)[0]), interpolation=cv2.INTER_NEAREST)
    cv2.imshow(name, img_res)
    cv2.waitKey(time)

def saveImage(image,folder,name):
    cv2.imwrite(folder+'/'+str(name)+'.png', image)