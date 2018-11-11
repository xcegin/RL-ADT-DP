from copy import deepcopy
from math import sqrt

from ADT.ADTNode import ADTNode


class LoopNode(ADTNode):

    def __init__(self, id, condition, nodeBlock):
        super().__init__(id)
        self.condition = condition
        self.nodeBlock = nodeBlock

    def accept(self, visitor):
        return visitor.visit_loop(self)

    def return_vector(self, visitor):
        listOfChildVectors = [self.condition.accept(visitor), self.nodeBlock.accept(visitor)]
        numOfTimes = int(round(sqrt(len(listOfChildVectors)))) + 1
        for x in range(numOfTimes):
            toBeAppended = deepcopy(listOfChildVectors)
            listOfChildVectors = listOfChildVectors + toBeAppended
        return listOfChildVectors
