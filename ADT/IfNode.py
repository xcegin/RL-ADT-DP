from copy import deepcopy

from ADT.ADTNode import ADTNode
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext
from constants import NUM_COPY_SUBLIST


class IfNode(ADTNode):
    CDTName = "c.CASTIfStatement"

    def __init__(self, id, condition, nodeThen, resolver_util, nodeElse=None):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition, resolver_util)
        self.nodeThen = resolveNodeViaType(nodeThen["$type"], nodeThen, resolver_util)
        if nodeElse is not None:
            self.nodeElse = resolveNodeViaType(condition["$type"], condition, resolver_util)
        else:
            self.nodeElse = None

    def accept(self, visitor):
        return visitor.visit_ifnode(self)

    def return_vector(self, visitor):
        from ADT.Visitors.AssigmentComplexityVisitor import AssigmentComplexityVisitor
        visitorComplexity = AssigmentComplexityVisitor(enviromentWalkerContext())
        from ADT.Visitors.RetrieveVariablesFromConditionVisitor import RetrieveVariablesFromConditionVisitor
        variablesUsedInCondition = RetrieveVariablesFromConditionVisitor(enviromentWalkerContext())
        self.condition.accept(visitorComplexity)
        self.condition.accept(variablesUsedInCondition)
        visitor.currentArgumentVectorDependency = variablesUsedInCondition.currentArguments
        lists = self.condition.accept(visitor)
        numOfTimes = int(visitorComplexity.complexityOfCurrExpression ** NUM_COPY_SUBLIST) + 1
        for x in range(numOfTimes):
            toBeAppended = deepcopy(lists)
            lists = lists + toBeAppended
        return []