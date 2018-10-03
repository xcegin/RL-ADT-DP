from enum import Enum

from ADT.ADTNode import ADTNode


class CTDOperatorsBitLogical(Enum):
    And = "op_logicalAnd"
    Or = "op_logicalOr"


class BinaryLogicalOperator(ADTNode):
    CTDOperatorsEnum = CTDOperatorsBitLogical

    def __init__(self, operation, leftOperand, rightOperand):
        self.operation = operation
        from ADT.ResolverUtil import resolveNodeViaType
        self.rightOperand = resolveNodeViaType(rightOperand["$type"], rightOperand)
        self.leftOperand = resolveNodeViaType(leftOperand["$type"], leftOperand)
