from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperators(Enum):
    Division = "op_divide"
    Subtraction = "op_minus"
    Modulus = "op_modulo"
    Multiplication = "op_multiply"
    Addition = "op_plus"

class BinaryArithmeticOperator(ADTNode):

    CTDOperatorsEnum = CTDOperators

    def __init__(self, astOperator, leftOperand, rightOperand):
        self.astOperator = astOperator
        self.rightOperand = rightOperand
        self.leftOperand = leftOperand