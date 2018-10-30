from ADT.ADTNode import ADTNode


class BinaryOperator(ADTNode):
    def __init__(self, operation, leftOperand, rightOperand):
        from ADT.ResolverUtil import resolveNodeViaType
        self.operation = operation
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)

    def accept(self, visitor):
        return visitor.visit_binaryoperator(self)

    def resolveOperationToString(self):
        return ""
