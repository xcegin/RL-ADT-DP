from abc import ABC

from ADT.ADTNode import ADTNode


class LoopNode(ABC, ADTNode):

    def __init__(self, condition, nodeBlock):
        self.condition = condition
        self.nodeBlock = nodeBlock
