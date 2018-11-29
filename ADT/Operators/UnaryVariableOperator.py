from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryVariableOperator(UnaryOperator):
    operations = {0: 'Dereference', 1: 'Address', 2: 'Sizeof'}

    def __init__(self, id, operation, operand):
        super().__init__(id, operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1