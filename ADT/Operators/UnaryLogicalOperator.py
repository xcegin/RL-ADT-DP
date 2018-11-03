from ADT.Operators.UnaryOperator import UnaryOperator



class UnaryLogicalOperator(UnaryOperator):
    operations = {0: 'Not'}

    def __init__(self, operation, operand):
        super().__init__(operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation