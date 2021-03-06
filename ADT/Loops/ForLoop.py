from copy import deepcopy
from math import sqrt

from ADT.Loops.LoopNode import LoopNode
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext
from constants import NUM_COPY_SUBLIST


class ForLoop(LoopNode):

    CDTName = "c.CASTForStatement"

    def __init__(self, id, nodeInit, condition, nodeAfter, nodeBlock, resolver_util):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition, resolver_util)
        self.nodeInit = resolveNodeViaType(nodeInit["$type"], nodeInit, resolver_util)
        self.nodeAfter = resolveNodeViaType(nodeAfter["$type"], nodeAfter, resolver_util)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock, resolver_util)

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
        from ADT.Visitors.AssigmentComplexityVisitor import AssigmentComplexityVisitor
        visitorComplexity = AssigmentComplexityVisitor(enviromentWalkerContext())
        from ADT.Visitors.RetrieveVariablesFromConditionVisitor import RetrieveVariablesFromConditionVisitor
        variablesUsedInCondition = RetrieveVariablesFromConditionVisitor(enviromentWalkerContext())
        self.condition.accept(visitorComplexity)
        self.condition.accept(variablesUsedInCondition)
        visitor.currentArgumentVectorDependency = variablesUsedInCondition.currentArguments
        listOfChildVectors += self.condition.accept(visitor)
        numOfTimes = int(visitorComplexity.complexityOfCurrExpression ** NUM_COPY_SUBLIST) + 1
        for x in range(numOfTimes):
            toBeAppended = deepcopy(listOfChildVectors)
            listOfChildVectors = listOfChildVectors + toBeAppended
        return listOfChildVectors

    def returnChildren(self):
        return [self.condition, self.nodeInit, self.nodeBlock, self.nodeAfter]
