from ADT.Loops.LoopNode import LoopNode


class ForLoop(LoopNode):

    CDTName = "c.CASTForStatement"

    def __init__(self, nodeInit, condition, nodeAfter, nodeBlock):
        from ADT.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeInit = resolveNodeViaType(nodeInit["$type"], nodeInit)
        self.nodeAfter = resolveNodeViaType(nodeAfter["$type"], nodeAfter)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)
