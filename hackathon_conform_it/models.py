from dataclasses import dataclass, field
from typing import List, Tuple, Dict



@dataclass
class Model:
    #name: str
    classe: str
    #templates: Dict[str, str] = field(default_factory=dict)
    bounding_box : List[Tuple[Tuple[int, int], int, int]] = field(default_factory=tuple)

    def load(self, name:str) -> 'any':
        pass
