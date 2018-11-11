from ADT.Operators.BinaryOperator import BinaryOperator


class BinaryArithmeticOperator(BinaryOperator):
    operations = {0: 'Addition', 1: 'Substraction', 2: 'Multiplication', 3: 'Division', 4: 'Modulus'}

    def __init__(self, id, operation, leftOperand, rightOperand):
        super().__init__(id, operation, leftOperand, rightOperand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation
