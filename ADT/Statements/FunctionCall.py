from ADT.ADTNode import ADTNode


# TODO: This should be replaced with an entire ADT structure of the called function
class FunctionCall(ADTNode):
    CDTName = "c.CASTFunctionCallExpression"
    CDTChildFunction = "c.CASTIdExpression"

    def __init__(self, name, arguments):
        self.name = name
        from ADT.ArgumentResolver import resolveArguments
        self.arguments = resolveArguments(arguments)
