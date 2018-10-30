from ADT.ADTNode import ADTNode


class UnaryOperator(ADTNode):


    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)

    def accept(self, visitor):
        return visitor.visit_unaryoperator(self)

    def resolveOperationToString(self):
        return ""