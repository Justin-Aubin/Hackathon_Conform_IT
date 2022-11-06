from nodes import Node
from typing import List


def link_lines_to_obj(things: List[Node], links:List[Node]) -> None:
    for th in things:
        for lk in links:
            if Node.collide(th, lk) and Node.compatible(th, lk):
                if lk.name == 'arrow':
                    lk.followers.append(th)
                    th.previouses.append(lk)
                else:
                    th.followers.append(lk)
                    lk.previouses.append(th)
                    

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
                    