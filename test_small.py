import cv2
from Region import Region


rows = 3
cols = 3

pixels = []

for i in range(rows):
    row = []
    for j in range(cols):
        reg = Region(True,10*(j+1))
        row.append(reg)
    pixels.append(row)

for r in range(rows):
    for c in range(cols):
        pixel = pixels[r][c]
        if r != 0:
            nb = pixels[r-1][c]
            pixel.addNeighbor(nb,0)
        if r != 2:
            nb = pixels[r+1][c]
            pixel.addNeighbor(nb, 2)
        if c != 0:
            nb = pixels[r][c-1]
            pixel.addNeighbor(nb, 3)
        if c != 2:
            nb = pixels[r][c+1]
            pixel.addNeighbor(nb, 1)


for r in range(rows):
    for c in range(cols):
        pixel = pixels[r][c]
        pixel.calc_weights()


def coarse_0(pixels):
    regions = []
    for r in range(rows):
        for c in range(cols):
            pixel = pixels[r][c]
            if pixel.parent is None:
                G1 = Region()
                G1.addSubregion(pixel)
                for sr in G1.subregions:
                    for nb in sr.neighbors:
                        if nb.parent is None:
                            res = nb.computeProbabilityofC()
                            if res > 0.4:
                                G1.addSubregion(nb)
                regions.append(G1)
    return regions

regions = coarse_0(pixels)


def process_neighbors(regions):
    for r in regions:
        r.processNeighbors()

process_neighbors(regions)

regions[0].calc_weights()

print("Ok")

