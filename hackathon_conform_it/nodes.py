from dataclasses import dataclass, field
from typing import List, Tuple, Dict

import numpy as np


@dataclass
class Node:
    id:str
    type:str
    ref: str
    thresh: int = 1
    connections: Tuple[tuple, tuple] | None = field(default_factory=tuple)
    corner: Tuple[int, int] = field(default_factory=tuple)
    h: int = 0
    w: int = 0    
    previouses: Dict[str, 'Node'] = field(default_factory=dict)
    followers: Dict[str, 'Node'] = field(default_factory=dict)
    name: str = None
    description: str = None
    comments: List[str] = field(default_factory=list)
    img: np.array = None
    
    
    @classmethod
    def collide(self, n1: 'Node', n2:'Node') -> int:
        """
        return -1 if they don't collide, and 0, 1, 2, 3 for south, west, north, est collision
        """
        return n1.corner[0] + n1.w + n1.thresh >= n2.corner[0] - n2.thresh and \
            n1.corner[0] - n1.thresh <= n2.corner[0] + n2.w + n2.thresh and \
            n1.corner[1] + n1.h +  n1.thresh  >= n2.corner[1] - n1.thresh and \
            n1.corner[1] - n1.thresh <= n2.corner[1] + n2.h + n2.thresh
      
    @classmethod
    def compatible(self, n1: 'Node', n2: 'Node') -> bool:
        compatible = False
        for i in range(4):
            if (n1.connections[0][i] and n2.connections[1][i]) or (n1.connections[1][i] and n2.connections[0][i]):
                compatible = True
                i = 5
      
        return compatible
      
            
    @classmethod
    def _line(self, id:str, corner: Tuple[int, int], h:int, w:int, dep: Tuple[int, int, int, int], vers: Tuple[int, int, int, int], comment:str = None) -> 'Node':
        # 0 ne peut pas se connecter, 1 peut se connecter, 2 doit se connecter à un objet (fléche)
        lcl = Node(id, "line", None, corner=corner, h=h, w=w)
        if comment:
            lcl.comments.append(comment)
        lcl.connections = (dep, vers)
        return lcl
    
    @classmethod
    def thing(self, corner: Tuple[int, int], h:int, w:int, id="temp", ref=None, thresh=1, name=None, description=None) -> 'Node':
        lcl = Node(id, "object", ref,  thresh, 
                   ((1, 1, 1, 1), (1, 1, 1, 1)), 
                   corner, h, w, 
                   name=name, description=description)
        
        return lcl
    
    @classmethod
    def pipeline(self, lines: List['Node']) -> 'Node':
        if len(lines) <= 0:
            return None
        
        
        lcl = Node(lines[0].id, "pipe", None, 1, lines[0].connections, lines[0].corner,  lines[0].h, lines[0].w)
        
        predecessors, ids, successors, comments = [], [], [], []
        
        for l in lines:
            predecessors = predecessors + l.previouses
            ids.append(l.id)
            successors = successors + l.followers
            comments = comments + l.comments
            
        predecessors, successors, comments = list(set(predecessors)), list(set(successors)), list(set(comments))
        for id in ids:
            if id in predecessors:
                predecessors.remove(id)
            if id in successors:
                successors.remove(id)
                
        lcl.connections = ((0, 0, 0, 0), (0, 0, 0, 0))
        lcl.previouses = predecessors
        lcl.followers = successors
        lcl.comments = comments
        
        return lcl
                
        
    
        
