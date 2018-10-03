from ADT.ADTNode import ADTNode
from ADT.ResolverUtil import resolveNodeViaType


class IfNode(ADTNode):
    CDTName = "c.CASTIfStatement"

    def __init__(self, condition, nodeThen, nodeElse=None):
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeThen = resolveNodeViaType(nodeThen["$type"], nodeThen)
        if nodeElse is not None:
            self.nodeElse = resolveNodeViaType(condition["$type"], condition)
        else:
            self.nodeElse = None
