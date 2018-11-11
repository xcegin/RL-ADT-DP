from ADT.ADTNode import ADTNode
from ADT.Utils.VectorUtil import vectorizationTypeLiteral


class LiteralNode(ADTNode):
    CDTName = "c.CASTLiteralExpression"
    CDTPropertyKind = "Kind"
    CDTPropertyValue = "Value"

    def __init__(self, id, value, kind):
        super().__init__(id)
        self.value = value
        self.kind = kind

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def resolveVectorizationValue(self):
        return vectorizationTypeLiteral(self.kind)
