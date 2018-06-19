import cv2
from Region import Region



reg1 = Region(True,100,0)
reg2 = Region(True,100,1)

reg1.addNeighbor(reg2,0)
reg2.addNeighbor(reg1,2)

reg1.calc_weights()

print(reg1.weights)