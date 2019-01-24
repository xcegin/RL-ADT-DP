import numpy
from copy import deepcopy

from ADT.Statements.StatementNode import StatementNode
from ADT.Variables.VariableNode import VariableNode
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext
from constants import NUM_COPY_SUBLIST


class AssignmentStatement(StatementNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, id, variable, value, resolverUtil):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable, resolverUtil)
        self.value = resolveNodeViaType(value["$type"], value, resolverUtil)

    def accept(self, visitor):
        return visitor.visit_assigment(self)

    def return_vector(self, visitor):
        lists = []
        from ADT.Visitors.AssigmentComplexityVisitor import AssigmentComplexityVisitor
        visitorComplexity = AssigmentComplexityVisitor(enviromentWalkerContext())
        from ADT.Visitors.RetrieveVariablesFromConditionVisitor import RetrieveVariablesFromConditionVisitor
        variablesUsedInCondition = RetrieveVariablesFromConditionVisitor(enviromentWalkerContext())
        self.value.accept(visitorComplexity)
        if isinstance(self.variable, VariableNode):
            self.value.accept(variablesUsedInCondition)
            visitor.currentArgumentVectorDependency = variablesUsedInCondition.currentArguments + [self.variable.variableName]
            lists += self.make_vector(visitor)
            lists += self.value.accept(visitor)
            numOfTimes = int(visitorComplexity.complexityOfCurrExpression ** NUM_COPY_SUBLIST) + 1
            for x in range(numOfTimes):
                toBeAppended = deepcopy(lists)
                lists = lists + toBeAppended
        return lists

    def make_vector(self, visitor):
        vectors = []
        for argument in reversed(list(visitor.arguments.keys())):
            vector = numpy.zeros(shape=8)
            from ADT.Utils.VectorUtil import typeOfVectorData
            vector[0] = typeOfVectorData(self)
            vector[1] = self.resolveVectorizationValue()
            vector[2] = typeOfVectorData(self.variable)
            vector[3] = typeOfVectorData(self.value)
            vector[4] = self.variable.resolveVectorizationValue()
            vector[5] = self.value.resolveVectorizationValue()
            vector[6] = visitor.embedding
            from ADT.Utils.VectorUtil import resolve_argument_involvement
            vector[7] = resolve_argument_involvement(argument, visitor)
            vectors.insert(0, vector)
        return vectors

    def returnChildren(self):
        return [self.variable, self.value]
