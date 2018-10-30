from ADT.Operators.BinaryOperator import BinaryOperator

class BinaryBitwiseOperator(BinaryOperator):
    operations = {0: 'And', 1: 'Or', 2: 'Xor', 3: 'ShiftLeft', 4: 'ShiftRight'}

    def __init__(self, operation, leftOperand, rightOperand):
        super().__init__(operation, leftOperand, rightOperand)

    def resolveOperationToString(self):
        return self.operations[self.operation]