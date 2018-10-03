from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryArithmetic(Enum):
    Minus = "op_minus"
    Plus = "op_plus"
    PostIncrement = "op_postFixDecr"
    PostDecrement = "op_postFixIncr"
    PreIncrement = "op_preFixDecr"
    PreDecrement = "op_preFixIncr"


class UnaryArithmeticOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryArithmetic

    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)
