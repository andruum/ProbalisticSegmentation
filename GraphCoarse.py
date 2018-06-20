import numpy as np
from Region import Region

def image_to_graph(image):
    pixels = []
    for i in range(image.shape[0]):
        row = []
        for j in range(image.shape[1]):
            reg = Region(True, image[i,j])
            row.append(reg)
        pixels.append(row)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            pixel = pixels[r][c]
            if r != 0:
                nb = pixels[r - 1][c]
                pixel.addNeighbor(nb, 0)
            if r != 2:
                nb = pixels[r + 1][c]
                pixel.addNeighbor(nb, 2)
            if c != 0:
                nb = pixels[r][c - 1]
                pixel.addNeighbor(nb, 3)
            if c != 2:
                nb = pixels[r][c + 1]
                pixel.addNeighbor(nb, 1)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            pixel = pixels[r][c]
            pixel.calc_weights()


def process_neighbors(regions):
    for r in regions:
        r.processNeighbors()

def calc_weights(regions):
    for r in regions:
        r.calc_weights()

def coarse_0(pixels_regions):
    regions = []
    for r in range(len(pixels_regions)):
        for c in range(len(pixels_regions[0])):
            pixel = pixels_regions[r][c]
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

    #assign nighbors to new regions
    process_neighbors(regions)

    return regions