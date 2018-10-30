from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryArithmeticOperator(UnaryOperator):
    operations = {0: 'Minus', 1: 'Plus', 2: 'PostIncrement', 3: 'PostDecrement', 4: 'PreIncrement', 5: 'PreDecrement'}

    def __init__(self, operation, operand):
        super().__init__(operation, operand)

    def resolveOperationToString(self):
        return self.operations[self.operation]