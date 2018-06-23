import cv2
import numpy as np
import math

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


# def debug_region(reg,image,Gid):
#     if reg.pixel:
#         row = int(reg.id / SHAPEIMG[1])
#         col = reg.id - row * SHAPEIMG[1]
#         image[row, col] = Gid
#     else:
#         for sr in reg.subregions:
#             debug_region(sr,image,Gid)

# def debug(region):
#     image = np.zeros(SHAPEIMG)
#     for reg in region:
#         debug_region(reg,image,reg.id)
#     print(image)

def getImage(imgpath):
    image = cv2.imread(imgpath, 0)
    return image

def resizeImg(image):
    return cv2.resize(image, dsize=(getShapeForCalc(image.shape)[1],getShapeForCalc(image.shape)[0]), interpolation=cv2.INTER_NEAREST)

# def getTestArray(rows,cols):
#     image = np.zeros((rows,cols))
#
#     for r in range(image.shape[0]):
#         for c in range(image.shape[1]):
#             image[r,c] = 100 if c < SHAPEIMG[0]/2 else 0
#     return image


# def debugImageBoundary(Gs,image):
#     image_debug = np.zeros(image.shape)
#
#     for g in Gs:
#         bp = g.getBoundaryPixels()
#         for p in bp:
#             r = int(p.id / image.shape[1])
#             c = p.id - r * image.shape[1]
#             image_debug[r,c] = 255
#     showImage(image_debug)

def debugImagePixels(Gs,image):
    print("Found regions:",len(Gs))
    shape = getShapeForCalc(image.shape)
    for g in Gs:
        image_debug = np.zeros(shape)
        bp = g.getPixelsRegions()
        for p in bp:
            r = int(p.id / shape[1])
            c = p.id - r * shape[1]
            image_debug[r,c] = 255
        # showImage(image_debug,0)
        saveImage(image_debug,g.id)


def showImage(img,time=0, name = 'debug'):
    img_res = cv2.resize(img, dsize=(getShapeForDebug(img.shape)[1], getShapeForDebug(img.shape)[0]), interpolation=cv2.INTER_NEAREST)
    cv2.imshow(name, img_res)
    cv2.waitKey(time)

def saveImage(image,name):
    cv2.imwrite('./results/'+str(name)+'.png', image)