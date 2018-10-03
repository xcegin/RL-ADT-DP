from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsBitLogical(Enum):
    And = "op_logicalAnd"
    Or = "op_logicalOr"


class BinaryLogicalOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsBitLogical

    def __init__(self, astOperator, leftOperand, rightOperand):
        self.astOperator = astOperator
        self.rightOperand = rightOperand
        self.leftOperand = leftOperand
