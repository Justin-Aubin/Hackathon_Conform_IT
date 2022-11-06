"""Entry Point."""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template, peak_local_max

from models import Model
from trucNul import find_placement, tieArrowsObjects
from justinLib import *
from nodes import Node

def run():
    """Main."""
    FOLDER = "./img"
    IMG_PNG = "Test.png"
    img = load_image(f"{FOLDER}/{IMG_PNG}")

    object_list = []

    for template_name in {"Valve", "Compressor"}:
        object_list += getObjet(img, template_name)

        """while (True):
            ## Test
            result = match_template(img, template)
            coordonates = peak_local_max(result,min_distance=50)

            coordonates = remove_isolate_peak(coordonates, result)

            for i, j in coordonates:
                heatmap[i][j] += result[i][j]

            ## Augmentation des tailles
            t_heigh, t_width = template.shape
            i_heigh, i_width = img.shape

            t_heigh += 25
            t_width += 25

            template = cv.resize(template, (t_heigh, t_width))

            print(f"{t_heigh}, {t_width}")

            if t_heigh > i_heigh or t_width > i_width:
                break

        coordonates = peak_local_max(heatmap, min_distance=50)
        coordonates = remove_isolate_peak(coordonates, heatmap)
        print(coordonates)"""



    # print(object_list)

    ## Lines

    list_arrow = getArrows(img)

    # print(list_arrow)

    list_ligne = getLines(img)

    # print(list_ligne)

    list_arrow, list_ligne = merge_arrow_ligne(list_arrow, list_ligne)

    print(f"{list_arrow}, {list_ligne}")


    nodesObjects = [Node(o.classe, o) for o in object_list]
    nodesArrows = [Node(o.classe, o) for o in list_arrow]
    tieArrowsObjects(nodesObjects, nodesArrows)
    choosing = [o.equi() for o in nodesObjects]
    root_obj = nodesObjects[choosing.index(min(choosing))]
    nodesObjects[2].save(f"./tmp/out.json")


    afficher(img, object_list, list_arrow, list_ligne)

if __name__ == "__main__":
    run()
