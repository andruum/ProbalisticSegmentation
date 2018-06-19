import numpy as np



class Region:

    def __init__(self,pixel=False,value = 0,pos = 0):
        self.subregions = []
        self.pixel = pixel
        self.id_pixel_pos = pos
        self.value = value
        self.neighbors = []
        self.directions = []

    def getIntensity(self):
        if self.pixel:
            return self.value
        else:
            # add scale matrix

    def getEdgeResponse(self):
        res = []
        if self.pixel:
            res = [0,0,0,0]
            for nb,dir in zip(self.neighbors,self.directions):
                res[dir] = abs(nb.value-self.value)
        else:
            #go deep
        return res

    def getPixels(self):
        pixels = []
        if self.pixel:
            pixels.append(self.value)
        else:
            for sr in self.subregions:
                pixels.extend(sr.getPixels())
        return pixels

    def getHist(self):
        pixels = self.getPixels()
        return np.bincount(pixels,minlength=256)/256

    # direction 0,1,2,3
    def addNeighbor(self,region,direction=-1):
        if self.pixel:
            if direction == -1:
                print("Error direction == -1 for pixel")
            self.directions.append(direction)
        self.neighbors.append(region)

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
            for ri in self.subregions:
                for rj in region.regions:
                    res += ri.getCommonLen(rj)
        else:
            for pi in self.neighbors:
                for pj in region.neighbors:
                    res += 1 if (pi == pj) else 0
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