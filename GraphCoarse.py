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

    # print(image.shape)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            pixel = pixels[r][c]
            if r != 0:
                nb = pixels[r - 1][c]
                pixel.addNeighbor(nb, 0)
            if r != image.shape[0]-1:
                nb = pixels[r + 1][c]
                pixel.addNeighbor(nb, 2)
            if c != 0:
                nb = pixels[r][c - 1]
                pixel.addNeighbor(nb, 3)
            if c != image.shape[1]-1:
                nb = pixels[r][c + 1]
                pixel.addNeighbor(nb, 1)

    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            pixel = pixels[r][c]
            pixel.calc_weights()

    return pixels

def process_neighbors(regions):
    for r in regions:
        r.processNeighbors()

def calc_weights(regions):
    for r in regions:
        r.calc_weights()

PSI_MERGE = 0.4

def coarse_0(pixels_regions):
    regions = []
    for r in range(len(pixels_regions)):
        for c in range(len(pixels_regions[0])):
            pixel = pixels_regions[r][c]
            if pixel.parent is None:
                G1 = Region()
                G1.addSubregion(pixel)
                T = np.zeros((len(pixels_regions) * len(pixels_regions[0]), 1))
                for sr in G1.subregions:
                    for nb in sr.neighbors:
                        if nb.parent is None:
                            res = nb.computeProbabilityofC(G1)
                            if res > PSI_MERGE:
                                G1.addSubregion(nb)
                                #addT = np.zeros((len(pixels_regions) * len(pixels_regions[0]), 1))
                                # print(addT.shape)
                                # print(T.shape)
                                #T = np.concatenate([T,addT],1)
                G1.T = T
                regions.append(G1)



    # for G1 in regions:
    #     for sr in G1.subregions:
    #         for r in range(len(pixels_regions)):
    #             for c in range(len(pixels_regions[0])):
    #                 pixel = pixels_regions[r][c]
    #                 if pixel.parent == G1:
    #                     G1.T[len(pixels_regions[0]) * r + c] = 1
    #                 elif sr.isNeighbor(pixel):
    #                     G1.T[len(pixels_regions[0]) * r + c] = pixel.coarseNeighborhood(sr)

    for r in range(len(pixels_regions)):
        for c in range(len(pixels_regions[0])):
            pixel = pixels_regions[r][c]

            for G1 in regions:
                if pixel in G1.subregions:
                    G1.T[len(pixels_regions[0])*r+c] = 1
                else:
                    for subregion in G1.subregions:
                        if subregion.isNeighbor(pixel):
                            G1.T[len(pixels_regions[0]) * r + c] = pixel.coarseNeighborhood(subregion)


    #assign nighbors to new regions
    process_neighbors(regions)
    # calc_weights(regions)

    return regions