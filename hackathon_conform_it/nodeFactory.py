from nodes import Node
from models import Model
from typing import List


class NodeFactory:
    
    count = 0
     
    @classmethod 
    def reset_count(self) -> None:
        self.count = 0
        
    @classmethod
    def get_line(self, model: Model) -> Node:
        cross = False
        entry = None
        match model.name:
            case 'lineHorizontal':
                entry = (0, 1, 0, 1)
            case 'lineVertical':
                entry = (1, 0, 1, 0)
            case 'arrowHorizontal':
                entry = (0, 1, 0, 1)
            case 'arrowVertical':
                entry = (1, 0, 1, 0)
            case 'corner0':
                entry = (1, 1, 0, 0)
            case 'corner1':
                entry = (0, 1, 1, 0)
            case 'corner2':
                entry = (0, 0, 1, 1)
            case 'corner3':
                entry = (1, 0, 0, 1)
            case 'cross':
                cross = True
            case other:
                return None
            
        fakeCoord = (0, 0)
        fakeh, fakew = 0, 0
        
        if cross:
            id1 = "{}_{}_{}".format(model.name, model.classe, self.count)
            self.count += 1
            id2 = "{}_{}_{}".format(model.name, model.classe, self.count)
            self.count += 1
            return [Node._line(id1, fakeCoord, fakeh, fakew, (0, 1, 0, 1), (0, 1, 0, 1)), Node._line(id2, fakeCoord, fakeh, fakew, (1, 0, 1, 0), (1, 0, 1, 0))]
        
        
        id = "{}_{}_{}".format(model.name, model.classe, self.count)
        self.count += 1
        return [Node._line(id, fakeCoord, fakeh, fakew, entry, entry)]
    
    # def get_cross(self, model:Model) -> Node:
    #     # to implement
    #     pass
    
    @classmethod
    def get_thing(self, model: Model) -> Node:
        id = "{}_{}_{}".format(model.name, model.classe, self.count)
        fakeCoord = (0, 0)
        fakeh, fakew = 0, 0
        
        return Node.thing(fakeCoord, fakeh, fakew, id)
    
    @classmethod
    def Lines(self, models:List[Model]) -> List[Node]:
        self.reset_count()
        output = []
        for model in models:
            output.append(self.get_line(model))
        return output
    
    
    @classmethod
    def Things(self, models:List[Model]) -> List[Node]:
        self.reset_count()
        output = []
        for model in models:
            output.append(self.get_thing(model))
        return output
    
    @classmethod
    def fun(self):
        self.reset_count()

        