import numpy
from copy import deepcopy

from ADT.Statements.StatementNode import StatementNode
from ADT.Utils.VectorUtil import typeOfVectorData, resolve_argument_involvement
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext


class VariableDeclarationStatement(StatementNode):

    CDTName = "c.CASTDeclarationStatement"
    CDTChildFunction = "c.CASTParameterDeclaration"
    CDTChildParameter = "c.CASTSimpleDeclaration"
    CDTChildInitializer = "c.CASTEqualsInitializer"

    def __init__(self, id, variableType, initialValue=None):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        if variableType is None:
            from ADT.UnknowNode import UnknownNode
            self.variableType = UnknownNode("unknown")
        else:
            self.variableType = resolveNodeViaType(variableType["$type"], variableType)
        self.variable = None
        if isinstance(initialValue,dict) and "$type" in initialValue:
            self.initialValue = resolveNodeViaType(initialValue["$type"], initialValue)
        else:
            self.initialValue = initialValue

    def accept(self, visitor):
        return visitor.visit_variabledeclaration(self)

    def return_vector(self, visitor):
        lists = []
        from ADT.Visitors.AssigmentComplexityVisitor import AssigmentComplexityVisitor
        visitorComplexity = AssigmentComplexityVisitor(enviromentWalkerContext())
        from ADT.LiteralNode import LiteralNode
        from ADT.Variables.VariableNode import VariableNode
        lists += self.make_vector(visitor)
        if self.initialValue is not None or not isinstance(self.initialValue, LiteralNode) or\
                not isinstance(self.initialValue, VariableNode):
            self.initialValue.accept(visitorComplexity)
            visitor.currentArgumentVectorDependency = self.variable.variableName
            lists += self.initialValue.accept(visitor)
            numOfTimes = int(visitorComplexity.complexityOfCurrExpression ** (1 / 4)) + 1
            for x in range(numOfTimes):
                toBeAppended = deepcopy(lists)
                lists += toBeAppended
        return lists

    def make_vector(self, visitor):
        #TODO: Rework last entry in vector
        vectors = []
        for argument in reversed(list(visitor.arguments.keys())):
            vector = numpy.zeros(shape=8)
            vector[0] = typeOfVectorData(self)
            vector[1] = self.resolveVectorizationValue()
            vector[2] = typeOfVectorData(self.variable)
            vector[3] = typeOfVectorData(self.initialValue)
            vector[4] = self.variable.resolveVectorizationValue()
            vector[5] = self.initialValue.resolveVectorizationValue() if self.initialValue is not None else 0
            vector[6] = visitor.embedding
            vector[7] = resolve_argument_involvement(argument, visitor)
            vectors.insert(0, vector)
        return vectors