from ADT.Operators.BinaryOperator import BinaryOperator


class BinaryLogicalOperator(BinaryOperator):
    operations = {0: 'And', 1: 'Or'}

    def __init__(self, id, operation, leftOperand, rightOperand, resolver_util):
        super().__init__(id, operation, leftOperand, rightOperand, resolver_util)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1
