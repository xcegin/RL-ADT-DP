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

    def __init__(self, operation, leftOperand, rightOperand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)