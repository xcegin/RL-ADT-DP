from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsUnaryVariable(Enum):
    Address = "op_amper"
    Dereference = "op_star"
    Sizeof = "op_sizeof"


class UnaryVariableOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsUnaryVariable

    def __init__(self, astOperator, operand):
        self.astOperator = astOperator
        self.operand = operand
