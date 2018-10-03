from ADT.ADTNode import ADTNode
from ADT.ArgumentResolver import resolveArguments


class FunctionDeclarationStatement(ADTNode):

    CDTName = "c.CASTFunctionDefinition"
    CDTChildFunction = "c.CASTFunctionDeclarator"
    CDTChildParameter = "c.CASTParameterDeclaration"

    def __init__(self, returnTypeModifiers, returnType, name, arguments, body):
        self.returnTypeModifiers = returnTypeModifiers
        self.returnType = returnType
        self.name = name
        self.arguments = resolveArguments(arguments)
        from ADT.ResolverUtil import resolveNodeViaType
        self.body = resolveNodeViaType(body["$type"], body["Nodes"])