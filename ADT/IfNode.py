from ADT.ADTNode import ADTNode


class IfNode(ADTNode):
    CDTName = "c.CASTIfStatement"

    def __init__(self, condition, nodeThen, nodeElse=None):
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeThen = resolveNodeViaType(nodeThen["$type"], nodeThen)
        if nodeElse is not None:
            self.nodeElse = resolveNodeViaType(condition["$type"], condition)
        else:
            self.nodeElse = None

    def accept(self, visitor):
        return visitor.visit_ifnode(self)