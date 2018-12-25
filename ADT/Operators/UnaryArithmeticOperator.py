from ADT.Operators.UnaryOperator import UnaryOperator


class UnaryArithmeticOperator(UnaryOperator):
    operations = {0: 'Minus', 1: 'Plus', 2: 'PostIncrement', 3: 'PostDecrement', 4: 'PreIncrement', 5: 'PreDecrement'}

    def __init__(self, id, operation, operand, resolver_util):
        super().__init__(id, operation, operand, resolver_util)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1