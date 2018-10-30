from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryVariableOperator(UnaryOperator):
    operations = {0: 'Dereference', 1: 'Address', 2: 'Sizeof'}

    def __init__(self, operation, operand):
        super().__init__(operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]