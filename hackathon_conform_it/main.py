"""Entry Point."""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template, peak_local_max

from models import Model
from trucNul import find_placement, tieArrowsObjects
from justinLib import *
from nodes import Node

Path_To_Symbols = "./tmp/"

def run():
    """Main."""
    FOLDER = "./img"
    IMG_PNG = "Test"

    object_list = []

    #for IMG_PNG in DATASET:
    img = load_image(f"{FOLDER}/{IMG_PNG}.png")
    for template_name in {"Valve", "Compressor"}:
        object_list += getObjet(img, Path_To_Symbols + template_name)

        print(object_list)

        ## Lines

        list_arrow = getArrows(img)

        # print(list_arrow)

        list_ligne = getLines(img)

        # print(list_ligne)

        list_arrow, list_ligne = merge_arrow_ligne(list_arrow, list_ligne)

        print(f"{list_arrow}, {list_ligne}")

        afficher(img, object_list, list_arrow, list_ligne)

        nodesObjects = [Node(o.classe, o) for o in object_list]
        nodesArrows = [Node(o.classe, o) for o in list_arrow]
        tieArrowsObjects(nodesObjects, nodesArrows)
        choosing = [o.equi() for o in nodesObjects]
        root_obj = nodesObjects[choosing.index(min(choosing))]
        nodesObjects[2].save(f"./tmp/out.json")

if __name__ == "__main__":
    run()
