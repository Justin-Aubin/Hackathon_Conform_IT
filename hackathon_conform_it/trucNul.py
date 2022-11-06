from justinLib import is_intersection
from nodes import Node


def pir(coord, box):
    return coord[0] >= box[0] and coord[0] <= box[0] + box[2] and \
        coord[1] >= box[1] and coord[1] <= box[1] + box[3]

def yolo_intersect(n1, n2, strict=True):
    box1o, box2o = n1.model.bounding_box, n2.model.bounding_box
    box1 = (box1o[0][0], box1o[0][1], box1o[1], box1o[2])
    box2 = (box2o[0][0], box2o[0][1], box2o[1], box2o[2])

    
    return is_intersection(box1, box2, strict=True)

def find_placement(box1o, box2o, direction, collision=False):
    box1 = (box1o[0][0], box1o[0][1], box1o[1], box1o[2])
    box2 = (box2o[0][0], box2o[0][1], box2o[1], box2o[2])
    EPS = 15

    if (direction == (1, 3)):
        # y0 de la flèche proche Y0 + h du node
        if abs(box2[0] - (box1[0] + box1[2])) <= 2 * EPS:
            return 1
        elif abs(box1[0] - (box2[0] + box2[2])) <= 2 * EPS:
            return -1
        elif collision and (box1[0] + box1[2] >= box2[0]):
            return -1
        elif collision and (box2[0] + box2[2] >= box1[0]):
            return 1

        
    return 0
        


def tieArrowsObjects(nobj_list, narrow_list):
    arrow_done = [0 for j in narrow_list]
    adresses = [0 for j in narrow_list]
    for nobj in nobj_list:
        for j, narrow in enumerate(narrow_list):
            if arrow_done[j] != 2:
                test = find_placement(narrow.model.bounding_box, nobj.model.bounding_box, narrow.model.from_to, yolo_intersect(narrow, nobj, False))

                if test == 1:

                    nobj.predArrow.append(narrow.id)
                    narrow.succs.append(nobj)
                    arrow_done[j] += 1
                elif test == -1:
                    nobj.successArrow.append(narrow.id)
                    narrow.preds.append(nobj)
                    arrow_done[j] += 1

                    
    for j in range(len(arrow_done)):
        if arrow_done[j] == 2:
            narrow_list[j].succs[0].preds.append(narrow_list[j].preds[0])
            narrow_list[j].preds[0].succs.append(narrow_list[j].succs[0])
                            

