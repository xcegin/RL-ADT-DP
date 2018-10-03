from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryLogical(Enum):
    Not = "op_not"


class UnaryLogicalOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryLogical

    def __init__(self, astOperator, operand):
        self.astOperator = astOperator
        self.operand = operand
