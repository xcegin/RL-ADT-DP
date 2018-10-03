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

    def __init__(self, operation, leftOperand, rightOperand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)