import numpy as np
import math
import probability_framework



def getTextureDifference(Ri, Rj):
    hi = Ri.getEdgeResponse()
    hj = Rj.getEdgeResponse()
    Dij = 0
    for i in range(len(hi)):
        if abs(hi[i]) + abs(hj[i]) != 0:
            Dij += math.pow((hi[i] - hj[i]) / (hi[i] + hj[i]), 2)
        else:
            Dij += 0
    return Dij

def getCommonLen(Ri,Rj):
    res = 0
    if Ri.pixel != Rj.pixel:
        raise Exception("Regions has different type")

    if not Ri.pixel:
        for sri in Ri.subregions:
            for srj in Rj.subregions:
                res += getCommonLen(sri,srj)
    else:
        for pj in Rj.neighbors:
            # print("ids",self.id,pi.id,pj.id)
            res += 1 if (Ri == pj) else 0
    return res

class Region:
    def __init__(self,pixel=False,value = -1, id = -1):
        self.weights = []
        self.subregions = []
        self.pixel = pixel
        self.value = value
        self.neighbors = []
        self.directions = []
        self.parent = None

        self.id  = id
        self.T = None
        self.edges_res = None

    def addSubregion(self, subregion):
        self.subregions.append(subregion)
        subregion.parent = self

    def getIntensity(self):
        if self.pixel:
            return self.value
        else:
            return self.value

    def getEdgeResponse(self):
        if self.pixel:
            if self.edges_res is None:
                self.edges_res = [0,0,0,0]
                for nb,dir in zip(self.neighbors,self.directions):
                    self.edges_res[dir] = abs(nb.value-self.value)
            return self.edges_res
        else:
            return self.edges_res

    def getTextureDifferenceP(self):
        Dijs = []
        for nb in self.neighbors:
            Dijs.append(getTextureDifference(self,nb))

        res = min(Dijs)
        return res

    def getTextureDifferenceM(self):
        len_d = 0
        for nb in self.neighbors:
            len_d += getCommonLen(self,nb) * getTextureDifference(self,nb)
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
        return np.bincount([len(pixels)])/len(pixels)

    # direction 0 upper ,1 right ,2 down ,3 left. for pixels
    def addNeighbor(self,region,direction=-1):
        if self.pixel:
            if direction == -1:
                print("Error direction == -1 for pixel")
            self.directions.append(direction)
        self.neighbors.append(region)

    def calc_weights(self):
        for R in self.neighbors:
            self.weights.append(probability_framework.prob_sp(self,R))

    def getTotalBoundary(self):
        res = 0
        for n in self.neighbors:
            res += getCommonLen(self,n)
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
            len_d += getCommonLen(self,nb)*abs(self.getIntensity() - nb.getIntensity())
        res = len_d/self.getTotalBoundary()
        return res

    def computeProbabilityofC(self, target_parent):
        cp = 0
        vp = 0
        for nb,w in zip(self.neighbors,self.weights):
            if nb.parent == target_parent:
                cp += w
            vp += w
        return cp/vp

    def processNeighbors(self):
        for sr in self.subregions:
            for nb in sr.neighbors:
                if nb.parent != self and nb.parent not in self.neighbors:
                    self.addNeighbor(nb.parent)

    def isNeighbor(self,other):
        return True if other in self.neighbors else False

    def coarseNeighborhood(self,Cregion):
        p = 0
        psum = 0
        for nb,w in zip(self.neighbors,self.weights):
            if Cregion == nb:
                p = w
            psum+=w
        return p/psum
