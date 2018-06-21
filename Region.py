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

    if Ri.pixel == False:
        for sri in Ri.subregions:
            for srj in Rj.subregions:
                if sri.pixel == False:
                    res += getCommonLen(sri,srj)

    else:
        for pj in Rj.neighbors:
            res += 1 if (Ri == pj) else 0
    return res

def getFreeLen(R):
    res = 0
    if not R.pixel:
        for sr in R.subregions:
            res += getFreeLen(sr)
    else:
        res += 4 - len(R.neighbors)
    return res


class Region:
    def __init__(self,pixel=False,value = -1, id = -1):
        self.weights = []
        self.subregions = []
        self.pixel = pixel
        self.value = int(value)
        self.neighbors = []
        self.directions = []
        self.parent = None

        self.id  = id
        self.T = None

        self.Ttqsum = 0
        self.Ttsum = 0

        self.edges_res = None
        self.externalPDifference_ = None
        self.externalMDifference_ = None
        self.total_boundaries = None
        self.pixels = None
        self.texture_diff_p = None
        self.texture_diff_m = None


    def addSubregion(self, subregion):
        self.subregions.append(subregion)
        subregion.parent = self


    def getPixels(self):
        if self.pixels is None:
            self.pixels = []
            if self.pixel:
                self.pixels.append(self.value)
            else:
                for sr in self.subregions:
                    self.pixels.extend(sr.getPixels())
        return self.pixels

    def getBoundaryPixels(self):
        if self.boundary_pixels is None:
            for p in self.pixels:
                if

        return self.boundary_pixels

    def getTotalPixels(self):
        if self.pixel:
            return 1
        return len(self.getPixels())

    # direction 0 upper ,1 right ,2 down ,3 left. for pixels
    def addNeighbor(self, region, direction=-1):
        if self.pixel:
            if direction == -1:
                print("Error direction == -1 for pixel")
            self.directions.append(direction)
        self.neighbors.append(region)

    def processNeighbors(self):
        for sr in self.subregions:
            for nb in sr.neighbors:
                if nb.parent != self and nb.parent not in self.neighbors:
                    self.addNeighbor(nb.parent)

    def isNeighbor(self,other):
        return True if other in self.neighbors else False

    def getTotalBoundary(self):
        if self.total_boundaries is None:
            self.total_boundaries = 0
            for n in self.neighbors:
                self.total_boundaries += getCommonLen(self,n)
            self.total_boundaries += getFreeLen(self)

        return self.total_boundaries

    def getIntensity(self):
        return self.value

    def getEdgeResponse(self):
        if self.pixel:
            if self.edges_res is None:
                self.edges_res = np.zeros((4,1))
                for nb,dir in zip(self.neighbors,self.directions):
                    self.edges_res[dir,0] = 2*abs(nb.value-self.value)
            return self.edges_res
        else:
            return self.edges_res



    def getTextureDifferenceP(self):
        if self.texture_diff_p is None:
            Dijs = []
            for nb in self.neighbors:
                Dijs.append(getTextureDifference(self,nb))
            self.texture_diff_p = min(Dijs)
        return self.texture_diff_p

    def getTextureDifferenceM(self):
        if self.texture_diff_m is None:
            len_d = 0
            for nb in self.neighbors:
                len_d += getCommonLen(self,nb) * getTextureDifference(self,nb)
            self.texture_diff_m = len_d / self.getTotalBoundary()

        return self.texture_diff_m




    def externalPDifference(self):
        if self.externalPDifference_ is None:
            diffs = []
            for nb in self.neighbors:
                dif = abs(self.getIntensity() - nb.getIntensity())
                diffs.append(dif)
            self.externalPDifference_ = min(diffs)

        return self.externalPDifference_

    def externalMDifference(self):
        if self.externalMDifference_ is None:
            len_d = 0
            for nb in self.neighbors:
                len_d += getCommonLen(self,nb)*abs(self.getIntensity() - nb.getIntensity())
            self.externalMDifference_ = len_d/(self.getTotalBoundary()-getFreeLen(self))

        return self.externalMDifference_




    def computeProbabilityofC(self, target_parent):
        cp = 0
        vp = 0
        for nb,w in zip(self.neighbors,self.weights):
            if nb.parent == target_parent:
                cp += w
            vp += w
        if vp == 0:
            return 0
        return cp/vp

    def calc_weights(self):
        for R in self.neighbors:
            id = R.neighbors.index(self)
            if len(R.weights)-1 == id:
                w = R.weights[id]
            else:
                w = probability_framework.prob_sp(self,R)
            self.weights.append(w)

    def coarseNeighborhood(self,Cregion):
        p = 0
        psum = 0
        for nb,w in zip(self.neighbors,self.weights):
            if Cregion == nb:
                p = w
            psum+=w
        if psum==0:
            return 0
        return p/psum

