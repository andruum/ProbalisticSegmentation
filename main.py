import GraphCoarse
import utils
import sys
import os

if __name__ == '__main__':

    if len(sys.argv) == 1:
        raise Exception('Specify path to image!')

    img_path = sys.argv[1]

    if not os.path.exists(img_path):
        raise Exception('Image not exists!')

    if len(sys.argv) == 3:
        max_regions = int(sys.argv[2])
    else:
        max_regions = 10

    image = utils.getImage(img_path)
    #utils.showImage(image, 1000, name = 'source')

    img_resized = utils.resizeImg(image)

    G0 = GraphCoarse.image_to_graph(img_resized)
    Gs = GraphCoarse.coarse_0(G0)

    while len(Gs)>max_regions:
        Gs = GraphCoarse.coarse(Gs)
        print("Current:",len(Gs))

    utils.debugImagePixels(Gs,image)
