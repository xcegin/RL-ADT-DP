from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsBitWise(Enum):
    And = "op_binaryAnd"
    Or = "op_binaryOr"
    Xor = "op_binaryXor"
    ShiftLeft = "op_shiftLeft"
    ShiftRight = "op_shiftRight"

class BinaryBitwiseOperator(ADTNode):

    CTDOperatorsEnum = CTDOperatorsBitWise

    def __init__(self, astOperator, leftOperand, rightOperand):
        self.astOperator = astOperator
        self.rightOperand = rightOperand
        self.leftOperand = leftOperand