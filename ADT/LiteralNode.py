from ADT.ADTNode import ADTNode


class LiteralNode(ADTNode):
    CDTName = "c.CASTLiteralExpression"
    CDTPropertyKind = "Kind"
    CDTPropertyValue = "Value"

    def __init__(self, value, kind):
        self.value = value
        self.kind = kind

    def accept(self, visitor):
        return visitor.visit_literal(self)
