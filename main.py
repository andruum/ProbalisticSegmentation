import cv2
from Region import Region


img = cv2.imread('test.jpg',0)

pixel_regions = []

# print(img.shape)
id = 0
for r in range(img.shape[0]):
    row = []
    for c in range(img.shape[1]):
        reg = Region(True,img[r,c],id)
        id+=1
        row.append(reg)
    pixel_regions.append(row)

for r in range(img.shape[0]):
    for c in range(img.shape[1]):
        pixel = pixel_regions[r][c]
        if r != 0:
            nb = pixel_regions[r-1][c]
            pixel.addNeighbor(nb,0)
        if r != img.shape[0]-1:
            nb = pixel_regions[r+1][c]
            pixel.addNeighbor(nb, 2)
        if c != 0:
            nb = pixel_regions[r][c-1]
            pixel.addNeighbor(nb, 3)
        if c != img.shape[1]-1:
            nb = pixel_regions[r-1][c]
            pixel.addNeighbor(nb, 1)

for r in range(img.shape[0]):
    for c in range(img.shape[1]):
        pixel = pixel_regions[r][c]
        pixel.calc_weights()

cv2.imshow('image',img)
k = cv2.waitKey(1000)


