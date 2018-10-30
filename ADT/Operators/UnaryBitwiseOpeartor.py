from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryBitwiseOperator(UnaryOperator):
    operations = {0: 'Negation'}

    def __init__(self, operation, operand):
        super().__init__(operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]