from ADT.ADTNode import ADTNode


class IfNode(ADTNode):
    CDTName = "c.CASTIfStatement"

    def __init__(self, id, condition, nodeThen, nodeElse=None):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeThen = resolveNodeViaType(nodeThen["$type"], nodeThen)
        if nodeElse is not None:
            self.nodeElse = resolveNodeViaType(condition["$type"], condition)
        else:
            self.nodeElse = None

    def accept(self, visitor):
        return visitor.visit_ifnode(self)

    def return_vector(self, visitor):
        return visitor.visit_ifnode(self)