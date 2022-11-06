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
def heatmap(image, template, scale):

    return None

def run():
    """Main."""
    FOLDER = "./img"
    IMG_PNG = "Test.png"
    img = load_image(f"{FOLDER}/{IMG_PNG}")

    object_list = []

    for template_name in {"Valve", "Compressor"}:
        template = load_image(f"./tmp/{template_name}.png", True)

        # heatmap = np.zeros(img.shape)
        hcoin, wcoin = template.shape

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

        ######## SKImage
        result = match_template(img, template)
        coordonates = peak_local_max(result,min_distance=10)

        ## Remove isolate peak
        coordonates = remove_isolate_peak(coordonates, result)

        ## Save Bounding box --> (x, y), h, w
        for coord in coordonates:
            object_list.append(Model(template_name, (coord, hcoin, wcoin)))

        fig = plt.figure()
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        ax1.imshow(img)
        ax1.set_axis_off()
        ax1.set_title("image")
        # highlight matched region
        for j, i in coordonates:
            rect = plt.Rectangle((i, j), wcoin, hcoin, edgecolor="r", facecolor="none")
            ax1.add_patch(rect)
            img = cv.rectangle(img, (i, j), (i + wcoin, j + hcoin), (255, 255, 255), -1)

        ax2.imshow(img)
        ax2.set_axis_off()
        ax2.set_title("`match_template`\nresult")

        plt.show()


    print(object_list)

    ## Lines


    list_lignes = []
    template = load_image(f"./tmp/1.png", True)
    ##### OpenCV
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.33
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        list_lignes.append(Model("ligne_h", (pt, pt[0] + w, pt[1] + h)))
    cv.imwrite("./tmp/res.png", img)

    print(list_lignes)

if __name__ == "__main__":
    run()
