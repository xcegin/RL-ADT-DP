from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryBitwise(Enum):
    Negation = "op_tilde"


class UnaryBitwiseOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryBitwise

    def __init__(self, astOperator, operand):
        self.astOperator = astOperator
        self.operand = operand
