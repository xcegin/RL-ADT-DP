from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryBitwiseOperator(UnaryOperator):
    operations = {0: 'Negation'}

    def __init__(self, id, operation, operand):
        super().__init__(id, operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation