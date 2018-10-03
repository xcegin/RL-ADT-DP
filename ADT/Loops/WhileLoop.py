from ADT.Loops.LoopNode import LoopNode


class WhileLoop(LoopNode):

    CDTName = "c.CASTWhileStatement"

    def __init__(self, condition, nodeBlock):
        self.condition = condition
        self.nodeBlock = nodeBlock
