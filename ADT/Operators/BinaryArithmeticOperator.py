from ADT.Operators.BinaryOperator import BinaryOperator

class BinaryArithmeticOperator(BinaryOperator):
    operations = {0: 'Addition', 1: 'Substraction', 2: 'Multiplication', 3: 'Division', 4: 'Modulus'}

    def __init__(self, operation, leftOperand, rightOperand):
        super().__init__(operation, leftOperand, rightOperand)

    def resolveOperationToString(self):
        return self.operations[self.operation]
