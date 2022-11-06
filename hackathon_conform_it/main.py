"""Entry Point."""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template, peak_local_max

from models import Model

@staticmethod
def load_image(path, is_template=False):
    if is_template:
        return cv.imread(path, 0)
    else:
        img = cv.imread(path)
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

@staticmethod
def remove_isolate_peak(coordonates, matrix):
    list = []
    for i, j in coordonates:
        if matrix[i][j] >= 0.75 * np.max(matrix):
            list.append((i, j))

    return list

@staticmethod
def effacer(image, coord, w, h):
    return cv.rectangle(image, coord, (coord[0] + w, coord[1] + h), (255, 255, 255), -1)

@staticmethod
def getObjet(img, template_name):
    template = load_image(f"./tmp/{template_name}.png", True)

    # heatmap = np.zeros(img.shape)
    hcoin, wcoin = template.shape
    list_objet = []

    ######## SKImage
    result = match_template(img, template)
    coordonates = peak_local_max(result,min_distance=10)

    ## Remove isolate peak
    coordonates = remove_isolate_peak(coordonates, result)

    ## Save Bounding box --> (x, y), h, w
    list_coord = []
    for coord in coordonates:
        list_coord.append((coord[0], coord[1], wcoin, hcoin))

    coordonates = merge_intersection(list_coord)

    for x, y, w, h in coordonates:
        list_objet.append(Model(template_name, ((x, y), w, h)))

    fig = plt.figure()
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    ax1.imshow(img)
    ax1.set_axis_off()
    ax1.set_title("image")
    # highlight matched region
    for j, i, w, h in coordonates:
        rect = plt.Rectangle((i, j), w, h, edgecolor="r", facecolor="none")
        ax1.add_patch(rect)
        img = effacer(img, (i, j), w, h)

    ax2.imshow(img)
    ax2.set_axis_off()
    ax2.set_title("`match_template`\nresult")

    plt.show()

    return list_objet

@staticmethod
def getArrows(image):
    list_arrow = []
    template = load_image(f"./tmp/arrow_1_3.png", True)
    ##### OpenCV
    w, h = template.shape[::-1]
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.33
    loc = np.where(res >= threshold)

    list_coords = []
    for pt in zip(*loc[::-1]):
        list_coords.append((pt[0], pt[1], w, h))

    coordonates = merge_intersection(list_coords)

    for x, y, w, h in coordonates:
        # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        list_arrow.append(Model("arrow", ((x, y), w, h), (1, 3)))

        image = effacer(image, (x, y), w, h)
    cv.imwrite("./tmp/res.png", image)

    return list_arrow

@staticmethod
def getLines(image):
    list_lines = []
    template = load_image(f"./tmp/line_h.png", True)
    ##### OpenCV
    w, h = template.shape[::-1]
    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.65
    loc = np.where(res >= threshold)

    list_coords = []
    for pt in zip(*loc[::-1]):
        list_coords.append((pt[0], pt[1], w, h))
        #cv.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv.imwrite("./tmp/res_line.png", image)

    coordonates = merge_intersection(list_coords)

    for x, y, w, h in coordonates:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        list_lines.append(Model("ligne", ((x, y), w, h), (1, 3)))
    cv.imwrite("./tmp/res.png", image)

    return list_lines

@staticmethod
def is_intersection(box1, box2):
    if ((box1[0] + box1[2] <= box2[0]) or (box2[0] + box2[2] <= box1[0])
        or (box1[1] + box1[3] <= box2[1]) or (box2[1] + box2[3] <= box1[1])):
        return False

    return True

@staticmethod
def merge_intersection(list_box):
    changement = True
    while changement:
        list_box, changement = test_and_merge(list_box)

    return list_box


@staticmethod
def test_and_merge(list_box):
    for i in range(len(list_box) - 1):
        box1 = list_box[i]

        for j in range(i + 1, len(list_box)):
            box2 = list_box[j]
            if is_intersection(box1, box2):
                # Bord Haut Gauche
                max_x = max(box1[0] + box1[2], box2[0] + box2[2])
                max_y = max(box1[1] + box1[3], box2[1] + box2[3])

                # Bord Bas Droit
                min_x = min(box1[0], box2[0])
                min_y = min(box1[1], box2[1])

                list_box[i] = (min_x, min_y, max_x - min_x, max_y - min_y)
                list_box.pop(j)
                return list_box, True

    return list_box, False

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



    print(object_list)

    ## Lines

    list_arrow = getArrows(img)

    print(list_arrow)

    list_ligne = getLines(img)

    print(list_ligne)

if __name__ == "__main__":
    run()
