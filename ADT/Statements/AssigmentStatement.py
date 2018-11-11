from copy import deepcopy

from ADT.Statements.StatementNode import StatementNode
from ADT.Variables.VariableNode import VariableNode
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext


class AssignmentStatement(StatementNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, id, variable, value):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.value = resolveNodeViaType(value["$type"], value)

    def accept(self, visitor):
        return visitor.visit_assigment(self)

    def return_vector(self, visitor):
        list = []
        from ADT.Visitors.AssigmentComplexityVisitor import AssigmentComplexityVisitor
        visitorComplexity = AssigmentComplexityVisitor(enviromentWalkerContext())
        self.value.accept(visitorComplexity)
        if self.variable is VariableNode:
            visitor.currentArgumentVectorDependency = self.variable.variableName
            list = self.value.accept(visitor)
            numOfTimes = int(visitorComplexity.complexityOfCurrExpression ** 1 / 4) + 1
            for x in range(numOfTimes):
                toBeAppended = deepcopy(list)
                list = list + toBeAppended
        return list