import numpy as np
from Region import Region
import configs



def image_to_graph(image):
    pixels = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            reg = Region(True, image[i,j],i*(image.shape[1])+j)
            pixels.append(reg)

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
            pixel.getEdgeResponse()

    calc_weights(pixels)

    return pixels

def process_neighbors(regions):
    for r in regions:
        r.processNeighbors()

def calc_weights(regions):
    print("Calc weights ",len(regions))
    for i,r in enumerate(regions):
        # print("Pixels ", len(r.subregions))
        r.calc_weights()
        # print(i/len(regions))


def coarse_0(pixels_regions):
    regions = []

    id = 0

    for pixel in pixels_regions:
        if pixel.parent is None:
            G1 = Region(id=id)
            id +=1
            G1.addSubregion(pixel)
            for sr in G1.subregions:
                for nb in sr.neighbors:
                    if nb.parent is None:
                        res = nb.computeProbabilityofC(G1)
                        if res > configs.PSI_MERGE:
                            G1.addSubregion(nb)
            regions.append(G1)

    for G1 in regions:
        tqsum = 0
        tesum = np.zeros((4,1))
        tsum = 0
        for pixel in G1.subregions:
            tsum += 1
            tqsum += pixel.value
            tesum += pixel.getEdgeResponse()
            for nb in pixel.neighbors:
                if nb.parent != G1:
                    tsum += nb.coarseNeighborhood(pixel)
                    tqsum += nb.coarseNeighborhood(pixel)*nb.value
                    tesum += nb.coarseNeighborhood(pixel)*nb.getEdgeResponse()

        G1.value = tqsum/tsum
        G1.edges_res = tesum/tsum

    #assign nighbors to new regions
    process_neighbors(regions)
    calc_weights(regions)

    return regions


def coarse(downregions):
    regions = []

    id = 0

    for dr in downregions:
        if dr.parent is None:
            G1 = Region(id=id)
            id +=1
            G1.addSubregion(dr)
            for sr in G1.subregions:
                for nb in sr.neighbors:
                    if nb.parent is None:
                        res = nb.computeProbabilityofC(G1)
                        if res > configs.PSI_MERGE:
                            G1.addSubregion(nb)
            regions.append(G1)

    for G1 in regions:
        tqsum = 0
        tesum = np.zeros((4,1))
        tsum = 0
        for sr in G1.subregions:
            tsum += 1*len(sr.subregions)
            tqsum += sr.value*len(sr.subregions)
            tesum += sr.getEdgeResponse()*len(sr.subregions)
            for nb in sr.neighbors:
                if nb.parent != G1:
                    tsum += nb.coarseNeighborhood(sr)*len(sr.subregions)
                    tqsum += nb.coarseNeighborhood(sr)*nb.value*len(sr.subregions)
                    tesum += nb.coarseNeighborhood(sr)*nb.getEdgeResponse()*len(sr.subregions)

        G1.value = tqsum/tsum
        G1.edges_res = tesum/tsum

    #assign nighbors to new regions
    process_neighbors(regions)
    calc_weights(regions)

    return regions