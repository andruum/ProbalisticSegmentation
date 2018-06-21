import numpy as np
from Region import Region


PSI_MERGE = 0.2

def image_to_graph(image):
    pixels = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            reg = Region(True, image[i,j],i*(image.shape[0])+j)
            pixels.append(reg)

    rows = image.shape[0]
    cols = image.shape[1]

    for i in range(len(pixels)):
            pixel = pixels[i]
            r = int(i/cols)
            c = i - r*cols
            if r != 0:
                id = (r-1)*cols+c
                nb = pixels[id]
                pixel.addNeighbor(nb, 0)
            if r != image.shape[0]-1:
                id = (r + 1) * cols + c
                nb = pixels[id]
                pixel.addNeighbor(nb, 2)
            if c != 0:
                id = r * cols + c-1
                nb = pixels[id]
                pixel.addNeighbor(nb, 3)
            if c != image.shape[1]-1:
                id = r * cols + c+1
                nb = pixels[id]
                pixel.addNeighbor(nb, 1)

    for pixel in pixels:
        pixel.calc_weights()

    return pixels

def process_neighbors(regions):
    for r in regions:
        r.processNeighbors()

def calc_weights(regions):
    for r in regions:
        r.calc_weights()



def calcQ0I(T,pixels):
    tqsum = 0
    tsum = 0
    for id,pv in enumerate(T):
        tqsum += pv*pixels[id].value
        tsum += pv
    return tqsum/tsum

def calcQsI(T,downregions):
    tqsum = 0
    tsum = 0
    for id,pv in enumerate(T):
        tqsum += pv*len(downregions[id].subregions)*downregions[id].value
        tsum += pv*len(downregions[id].subregions)
    return tqsum/tsum

def calcQ0E(T,pixels):
    tqsum = 0
    tsum = 0
    for id,pv in enumerate(T):
        tqsum += pv*pixels[id].getEdgeResponse()
        tsum += pv
    return tqsum/tsum

def calcQsE(T,downregions):
    tqsum = 0
    tsum = 0
    for id,pv in enumerate(T):
        tqsum += pv*len(downregions[id].subregions)*downregions[id].getEdgeResponse()
        tsum += pv*len(downregions[id].subregions)
    return tqsum/tsum

def coarse_0(pixels_regions):
    regions = []

    id = 0

    for pixel in pixels_regions:
        if pixel.parent is None:
            G1 = Region(id=id)
            id +=1
            G1.addSubregion(pixel)
            T = np.zeros((len(pixels_regions), 1))
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

    for i,pixel in enumerate(pixels_regions):
        for G1 in regions:
            if pixel in G1.subregions:
                G1.T[i] = 1
            else:
                for subregion in G1.subregions:
                    if subregion.isNeighbor(pixel):
                        G1.T[i] = pixel.coarseNeighborhood(subregion)


    for G1 in regions:
        G1.value = calcQ0I(G1.T,pixels_regions)
        G1.edges_res = calcQ0E(G1.T,pixels_regions)
    #assign nighbors to new regions
    process_neighbors(regions)
    calc_weights(regions)

    return regions

def coarse(downregions):
    regions = []

    id = 0
    for dr in downregions:
        if dr.parent is None:
            Gs = Region(id=id)
            id+=1
            Gs.addSubregion(dr)
            T = np.zeros((len(downregions), 1))
            for sr in Gs.subregions:
                for nb in sr.neighbors:
                    if nb.parent is None:
                        res = nb.computeProbabilityofC(Gs)
                        if res > PSI_MERGE:
                            Gs.addSubregion(nb)
            Gs.T = T
            regions.append(Gs)

    for i, pixel in enumerate(downregions):
        for Gs in regions:
            if pixel in Gs.subregions:
                Gs.T[i] = 1
            else:
                for subregion in Gs.subregions:
                    if subregion.isNeighbor(pixel):
                        Gs.T[i] = pixel.coarseNeighborhood(subregion)

    for Gs in regions:
        Gs.value = calcQsI(Gs.T, downregions)
        Gs.edges_res = calcQsE(Gs.T, downregions)
    # assign nighbors to new regions
    process_neighbors(regions)
    calc_weights(regions)

    return regions