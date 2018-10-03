from ADT.Loops.LoopNode import LoopNode


class WhileLoop(LoopNode):

    CDTName = "c.CASTWhileStatement"

    def __init__(self, condition, nodeBlock):
        from ADT.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)
