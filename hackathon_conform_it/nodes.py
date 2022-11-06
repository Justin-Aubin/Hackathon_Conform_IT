from dataclasses import dataclass, field
from typing import List, Tuple, Dict

import numpy as np
from models import Model
from secrets import token_hex 

@dataclass
class Node:
    nom:str
    model: Model
    id:str = field(default=None, repr=False)
    predArrow: List[str] = field(default_factory=list, repr=False)
    successArrow: List[str] = field(default_factory=list, repr=False)
    preds: List['Node'] = field(default_factory=list)
    succs: List['Node'] = field(default_factory=list)
    
    def __post_init__(self):
        id = token_hex(64)
    
    def count_preds(self):
        out = 0
        for p in  self.preds:
            out += p.count_preds()
        return out

    def count_succs(self):
        out = 0
        for p in  self.succs:
            out += p.count_succs()
        return out
    
    def equi(self):
        return abs(self.count_succs() - self.count_preds())