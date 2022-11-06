from justinLib import is_intersection
from nodes import Node


def pir(coord, box):
    return coord[0] >= box[0] and coord[0] <= box[0] + box[2] and \
        coord[1] >= box[1] and coord[1] <= box[1] + box[3]
        
def find_placement(box1o, box2o, direction):
    box1 = (box1o[0][0], box1o[0][1], box1o[1], box1o[2])
    box2 = (box2o[0][0], box2o[0][1], box2o[1], box2o[2])
    EPS = 15
    
    if (direction == (1, 3)):
        # y0 de la flèche proche Y0 + h du node 
        if abs(box2[0] - (box1[0] + box1[2])) <= 2 * EPS:
            return 1
        elif abs(box1[0] - (box2[0] + box2[2])) <= 2 * EPS:
            return -1
        
    return 0
        
    # a = (box1[0] + box1[2], box1[1])
    # b = (box1[0], box1[1])
    # c = (box1[0], box1[1] + box1[3])
    # d = (box1[0] + box1[2], box1[1] + box1[3])
    
    # resp = []
    # if pir(a, box2):
    #     resp.append(0)
    #     resp.append(1)
    # if pir(b, box2):
    #     resp.append(1)
    #     resp.append(2)
    # if pir(c, box2):
    #     resp.append(2)
    #     resp.append(3)
    # if pir(d, box2):
    #     resp.append(3)
    #     resp.append(0)
        
    # return list(set(resp))           

def tieArrowsObjects(nobj_list, narrow_list):
    arrow_done = [0 for j in narrow_list]
    for nobj in nobj_list:
        for j, narrow in enumerate(narrow_list):
            if arrow_done[j] != 2:
                test = find_placement(narrow.model.bounding_box, nobj.model.bounding_box, narrow.model.from_to)
                print("buhhhhh", test)
                if test == 1:
                    nobj.predArrow.append(narrow.id)
                    arrow_done[j] += 1
                elif test == -1:
                    nobj.successArrow.append(narrow.id)
                    arrow_done[j] += 1
                    
    for nobj1 in nobj_list:
        for j in range(len(arrow_done)):
            if arrow_done[j] == 2:
                for nobj2 in nobj_list:
                    if nobj1.id != nobj2.id:
                        if narrow_list[j] in nobj1.successArrow and narrow_list[j] in nobj2.predArrow:
                            nobj1.succs.append(nobj2)
                            
            
