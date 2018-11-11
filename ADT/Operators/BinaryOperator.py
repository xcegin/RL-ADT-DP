import numpy

from ADT.ADTNode import ADTNode
from ADT.Utils.VectorUtil import typeOfVectorData, resolve_argument_involvement


class BinaryOperator(ADTNode):
    def __init__(self, id, operation, leftOperand, rightOperand):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.operation = operation
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)

    def accept(self, visitor):
        return visitor.visit_binaryoperator(self)

    def resolveOperationToString(self):
        return ""

    def resolveVectorizationValue(self):
        return 0

    def return_vector(self, visitor):
        vectorsOfChildren = [self.leftOperand.accept(visitor), self.rightOperand.accept(visitor)]
        if len(vectorsOfChildren) == 0:
            return vectorsOfChildren
        for argument in reversed(list(visitor.arguments.keys())):
            vector = numpy.zeros(shape=8)
            vector[0] = typeOfVectorData(self)
            vector[1] = self.resolveVectorizationValue()
            vector[2] = typeOfVectorData(self.leftOperand)
            vector[3] = typeOfVectorData(self.rightOperand)
            vector[4] = self.leftOperand.resolveVectorizationValue()
            vector[5] = self.rightOperand.resolveVectorizationValue()
            vector[6] = visitor.embedding
            vector[7] = resolve_argument_involvement(argument, visitor)
            vectorsOfChildren.insert(0, vector)
        return vectorsOfChildren
