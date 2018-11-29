from ADT.Operators.UnaryOperator import UnaryOperator



class UnaryLogicalOperator(UnaryOperator):
    operations = {0: 'Not'}

    def __init__(self, id, operation, operand):
        super().__init__(id, operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1