from dataclasses import dataclass, field
from typing import List, Tuple, Dict

import numpy as np
from models import Model
from secrets import token_hex 
import json
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
        self.id = token_hex(64)
    
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
    
    def clean(self):
        for o in self.succs:
        #    cop = o.succs[:]
            indice = {i.id:i for i in o.preds}
            
            indice.pop(self.id, None)
            o.preds = list(indice.values())
            
        for o in self.preds:
            indice = {i.id:i for i in o.succs}
        
            indice.pop(self.id, None)
            o.succs = list(indice.values())

        for i in self.succs:
            i.clean()
        for i in self.preds:
            i.clean()
              
    def to_dict(self):
        dict = {
            "nom":self.nom,
            "input": [],
            "output": [],
        }       
        for i in self.succs:
            dict["input"].append(i.to_dict())
        for i in self.preds:
            dict["output"].append(i.to_dict())
            
        return dict
          
    def save(self, path):
        self.clean()
        dict = self.to_dict()
        with open(path, 'w') as f:
            json.dump(dict, f, indent=4)
        
           