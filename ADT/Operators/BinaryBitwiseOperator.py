from ADT.Operators.BinaryOperator import BinaryOperator

class BinaryBitwiseOperator(BinaryOperator):
    operations = {0: 'And', 1: 'Or', 2: 'Xor', 3: 'ShiftLeft', 4: 'ShiftRight'}

    def __init__(self, id, operation, leftOperand, rightOperand, resolver_util):
        super().__init__(id, operation, leftOperand, rightOperand, resolver_util)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1