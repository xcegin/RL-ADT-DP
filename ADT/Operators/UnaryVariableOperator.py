from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryVariable(Enum):
    Address = "op_amper"
    Dereference = "op_star"
    Sizeof = "op_sizeof"


class UnaryVariableOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryVariable

    def __init__(self, operation, operand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.operand = resolveNodeViaType(operand["$type"], operand)
