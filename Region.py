



class Region:

    def __init__(self,pixel=False,value = 0):
        self.subregions = []
        self.pixel = pixel
        self.value = value
        self.neighbors = []

    def getIntensity(self):
        if self.pixel:
            return self.value
        else:


    def addNeighbor(self,region):
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


class Pixel:

    def __init__(self,value,x,y):
        self.value = value
        self.x = x
        self.y = y

    def isNeighbor(self,pixel):
        dx = abs(pixel.x - self.x)
        dy = abs(pixel.y - self.y)
        if dx+dy == 1:
            return 1
        else:
            return 0