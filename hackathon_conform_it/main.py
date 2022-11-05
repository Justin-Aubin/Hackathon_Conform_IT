"""Entry Point."""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import match_template


def run():
    """Main."""
    folder = "./img"
    img_png = "SIMPLE-1.jpg"
    img = cv.imread(f"{folder}/{img_png}")
    template = cv.imread(f"./tmp/405.png", 0)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    """ _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)"""

    w, h = template.shape[::-1]
    res = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imwrite("./tmp/res.png", img)

    """i = 0
    for ctr in contours:
        i += 1

        x, y, w, h = cv2.boundingRect(ctr)
        if w > 15 and h > 15:
            roi = img[y:y+h, x:x+w]
            cv2.imwrite(f"{folder}/out/{img_png.split('.')[0]}/{str(i)}_out.jpg", filters.sobel(img))
    cv2.imshow('img',img)
    # cv2.waitKey(0)   """

    result = match_template(gray, template)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]

    fig = plt.figure(figsize=(8, 3))
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

    ax1.imshow(template, cmap=plt.cm.gray)
    ax1.set_axis_off()
    ax1.set_title("template")

    ax2.imshow(img, cmap=plt.cm.gray)
    ax2.set_axis_off()
    ax2.set_title("image")
    # highlight matched region
    hcoin, wcoin = template.shape
    rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor="r", facecolor="none")
    ax2.add_patch(rect)

    ax3.imshow(result)
    ax3.set_axis_off()
    ax3.set_title("`match_template`\nresult")
    # highlight matched region
    ax3.autoscale(False)
    ax3.plot(x, y, "o", markeredgecolor="r", markerfacecolor="none", markersize=10)

    plt.show()


if __name__ == "__main__":
    run()
