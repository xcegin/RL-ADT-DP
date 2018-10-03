from ADT.Loops.LoopNode import LoopNode


class DoLoop(LoopNode):

    CDTName = "c.CASTDoStatement"

    def __init__(self, condition, nodeBlock):
        self.condition = condition
        self.nodeBlock = nodeBlock
