from copy import deepcopy
from math import sqrt

from ADT.Loops.LoopNode import LoopNode


class ForLoop(LoopNode):

    CDTName = "c.CASTForStatement"

    def __init__(self, id, nodeInit, condition, nodeAfter, nodeBlock):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeInit = resolveNodeViaType(nodeInit["$type"], nodeInit)
        self.nodeAfter = resolveNodeViaType(nodeAfter["$type"], nodeAfter)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)

    def accept(self, visitor):
        return visitor.visit_forloop(self)

    def return_vector(self, visitor):
        initNodeVectors = self.nodeInit.accept(visitor)
        listOfChildVectors = [self.condition.accept(visitor), self.nodeBlock.accept(visitor),
                              self.nodeAfter.accept(visitor)]
        numOfTimes = int(round(sqrt(len(listOfChildVectors)))) + 1
        for x in range(numOfTimes):
            toBeAppended = deepcopy(listOfChildVectors)
            listOfChildVectors = listOfChildVectors + toBeAppended
        listOfChildVectors.insert(0, initNodeVectors)
        return listOfChildVectors