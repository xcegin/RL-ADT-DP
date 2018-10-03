from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryLogical(Enum):
    Not = "op_not"


class UnaryLogicalOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryLogical

    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)
