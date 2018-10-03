from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsComparison(Enum):
    Equals = "op_equals"
    GreaterThanEquals = "op_greaterEqual"
    GreaterThan = "op_greaterThan"
    LessThanEquals = "op_lessEqual"
    LessThan = "op_lessThan"
    NotEquals = "op_notequals"


class ComparisonOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsComparison

    def __init__(self, astOperator, leftOperand, rightOperand):
        self.astOperator = astOperator
        self.rightOperand = rightOperand
        self.leftOperand = leftOperand
