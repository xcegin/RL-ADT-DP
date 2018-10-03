from ADT.Variables.VariableNode import VariableNode


class ArraySubscriptVariable(VariableNode):

    CDTName = "c.CASTArraySubscriptExpression"

    def __init__(self, variableName, array, subscript):
        VariableNode.__init__(self, variableName)

        self.array = array
        self.subscript = subscript
