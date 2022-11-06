def pir(coord, box):
    return coord[0] >= box[0] and coord[0] <= box[0] + box[2] and \
        coord[1] >= box[1] and coord[1] <= box[1] + box[3]
        
def find_placement(box1, box2):
    a = (box1[0] + box1[2], box1[1])
    b = (box1[0], box1[1])
    c = (box1[0], box1[1] + box1[3])
    d = (box1[0] + box1[2], box1[1] + box1[3])
    
    resp = []
    if pir(a, box2):
        resp.append(0)
        resp.append(1)
    if pir(b, box2):
        resp.append(1)
        resp.append(2)
    if pir(c, box2):
        resp.append(2)
        resp.append(3)
    if pir(d, box2):
        resp.append(3)
        resp.append(0)
        
    return list(set(resp))