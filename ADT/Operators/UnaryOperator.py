import numpy

from ADT.ADTNode import ADTNode
from ADT.Utils.VectorUtil import typeOfVectorData, resolve_argument_involvement


class UnaryOperator(ADTNode):


    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)

    def accept(self, visitor):
        return visitor.visit_unaryoperator(self)

    def resolveOperationToString(self):
        return ""

    def resolveVectorizationValue(self):
        return 0

    def return_vector(self, visitor):
        vectorsOfChildren = [self.operand.accept(visitor)]
        if len(vectorsOfChildren) == 0:
            return vectorsOfChildren
        for argument in reversed(visitor.arguments):
            vector = numpy.zeros(shape=8)
            vector[0] = typeOfVectorData(self)
            vector[1] = self.resolveVectorizationValue()
            vector[2] = typeOfVectorData(self.operand)
            vector[3] = -1
            vector[4] = self.operand.resolveVectorizationValue()
            vector[5] = -1
            vector[6] = visitor.embedding
            vector[7] = resolve_argument_involvement(argument, visitor)
            vectorsOfChildren.insert(0, vector)
        return vectorsOfChildren