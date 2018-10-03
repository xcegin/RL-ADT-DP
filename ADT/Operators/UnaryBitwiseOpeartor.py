from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryBitwise(Enum):
    Negation = "op_tilde"


class UnaryBitwiseOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryBitwise

    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)
