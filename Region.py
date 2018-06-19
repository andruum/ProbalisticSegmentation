import numpy as np
import math
import probability_framework

class Region:

    def __init__(self,pixel=False,value = 0,id = -1):
        self.id = id
        self.weights = []
        self.subregions = []
        self.pixel = pixel
        self.value = value
        self.neighbors = []
        self.directions = []

    def getIntensity(self):
        if self.pixel:
            return self.value
        else:
            return 0
            # add scale matrix

    def getEdgeResponse(self):
        res = []
        if self.pixel:
            res = [0,0,0,0]
            for nb,dir in zip(self.neighbors,self.directions):
                res[dir] = abs(nb.value-self.value)
        else:
            pass
            #go deep
        return res

    def getTextureDifference(self,region):
        hi = self.getEdgeResponse()
        hj = region.getEdgeResponse()
        Dij = 0
        for i in range(4):
            Dij += math.pow((hi[i] - hj[i]) / (hi[i] + hj[i]), 2)

        return Dij

    def getTextureDifferenceP(self):
        Dijs = []

        for nb in self.neighbors:
            Dijs.append(self.getTextureDifference(nb))

        res = min(Dijs)
        return res

    def getTextureDifferenceM(self):
        len_d = 0
        for nb in self.neighbors:
            len_d += self.getCommonLen(nb) * self.getTextureDifference(nb)
        res = len_d / self.getTotalBoundary()

        return res


    def getPixels(self):
        pixels = []
        if self.pixel:
            pixels.append(self.value)
        else:
            for sr in self.subregions:
                pixels.extend(sr.getPixels())
        return pixels

    def getTotalPixels(self):
        return len(self.getPixels())

    def getHist(self):
        pixels = self.getPixels()
        return np.bincount(pixels,minlength=256)/256

    # direction 0 upper ,1 right ,2 down ,3 left
    def addNeighbor(self,region,direction=-1):
        if self.pixel:
            if direction == -1:
                print("Error direction == -1 for pixel")
            self.directions.append(direction)
        self.neighbors.append(region)

    def calc_weights(self):
        for R in self.neighbors:
            self.weights.append(probability_framework.prob_sp(self,R))


    def addSubregion(self, region):
        self.neighbors.append(region)

    def getTotalBoundary(self):
        res = 0
        for n in self.neighbors:
            res += self.getCommonLen(n)
        return res

    def getCommonLen(self,region):
        res = 0
        if not self.pixel:
            return 0
            # for ri in self.subregions:
            #     for rj in region.regions:
            #         res += ri.getCommonLen(rj)
        else:
            for pj in region.neighbors:
                # print("ids",self.id,pi.id,pj.id)
                res += 1 if (self.id == pj.id) else 0
        return res

    def externalPDifference(self):
        diffs = []
        for nb in self.neighbors:
            dif = abs(self.getIntensity() - nb.getIntensity())
            diffs.append(dif)
        res = min(diffs)
        return res

    def externalMDifference(self):
        len_d = 0
        for nb in self.neighbors:
            len_d += self.getCommonLen(nb)*abs(self.getIntensity() - nb.getIntensity())
        res = len_d/self.getTotalBoundary()
        return res

# class Pixel:
#
#     def __init__(self,value,x,y):
#         self.value = value
#         self.x = x
#         self.y = y
#
#     def isNeighbor(self,pixel):
#         dx = abs(pixel.x - self.x)
#         dy = abs(pixel.y - self.y)
#         if dx+dy == 1:
#             return 1
#         else:
#             return 0