from abc import ABC

from ADT.ADTNode import ADTNode


class VariableNode(ADTNode, ABC):

    def __init__(self, variableName=None):
        self.variableName = variableName
