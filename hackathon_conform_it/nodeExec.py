from nodes import Node
from typing import List


def link_lines_to_obj(things: List[Node], links:List[Node]) -> None:
    addedth, addedlk = [], []
    for th in things:
        for lk in links:
            if Node.collide(th, lk) and Node.compatible(th, lk):
                addedth.append(th)
                addedlk.append(lk)
                if lk.name == 'arrow':
                    lk.followers.append(th)
                    th.previouses.append(lk)
                else:
                    th.followers.append(lk)
                    lk.previouses.append(th)
    for lk in links:
        if lk not in addedlk:
            links.remove(lk)
    for th in things:
        if th not in addedth:
            things.remove(th)

    for th in things:
        th.previouses, th.followers = list(set(th.previouses)), list(set(th.followers))
    for lk in links:
        lk.previouses, lk.followers = list(set(lk.previouses)), list(set(lk.followers))
                   

def link_lines(lk: List[Node]) -> List[List[Node]]:
    added = []
    results = []
    for i in range(len(lk)):
        
        if not i in added:
            lcl = []
            lcl.append(lk[i])
            added.append(i)
            for j in range(i+1, len(lk)):
                if not j in added and Node.collide(lk[i], lk[j]) and Node.compatible(lk[i], lk[j]):
                    lcl.append(lk[j])
                    
            results.append(lcl)
            
            
    return results
                    