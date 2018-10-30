from ADT.Operators.BinaryOperator import BinaryOperator


class BinaryLogicalOperator(BinaryOperator):
    operations = {0: 'And', 1: 'Or'}

    def __init__(self, operation, leftOperand, rightOperand):
        super().__init__(operation, leftOperand, rightOperand)

    def resolveOperationToString(self):
        return self.operations[self.operation]