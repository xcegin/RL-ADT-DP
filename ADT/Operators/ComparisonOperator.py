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

    def __init__(self, operation, leftOperand, rightOperand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)
