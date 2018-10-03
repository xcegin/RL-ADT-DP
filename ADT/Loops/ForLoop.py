from ADT.Loops.LoopNode import LoopNode


class ForLoop(LoopNode):

    CDTName = "c.CASTForStatement"

    def __init__(self, nodeInit, condition, nodeAfter, nodeBlock):
        self.condition = condition
        self.nodeInit = nodeInit
        self.nodeAfter = nodeAfter
        self.nodeBlock = nodeBlock
