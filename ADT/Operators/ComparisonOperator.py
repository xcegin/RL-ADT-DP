from ADT.Operators.BinaryOperator import BinaryOperator


class ComparisonOperator(BinaryOperator):
    operations = {0: 'LessThan', 1: 'GreaterThan', 2: 'LessThanEquals', 3: 'GreaterThanEquals', 4: 'Equals',
                  5: 'NotEquals'}

    def __init__(self, id, operation, leftOperand, rightOperand):
        super().__init__(id, operation, leftOperand, rightOperand)

    def resolveOperationToString(self):
        return self.operations[self.operation]

    def resolveVectorizationValue(self):
        return self.operation + 1
