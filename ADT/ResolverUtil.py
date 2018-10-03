from ADT.IfNode import IfNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.UnknowNode import UnknownNode


def resolveType(type):
    startIndex = type.find('[')
    if startIndex > -1:
        endIndex = type.find[']']
        type = type[startIndex:endIndex]
        type = type.replace("[","")
        type = type.replace("]", "")

    givenType = type.split(',')[0]
    return givenType.split('.')[-1]

def resolveNodeViaType(type, node):
    if type == "VariableDeclarationStatement":
        return VariableDeclarationStatement(node["VariableTypeModifiers"], node["VariableType"],
                                            node["Variable"], node["InitialValue"])
    elif type == "IfNode":
        return IfNode(node["Condition"], node["NodeThen"], node["NodeElse"])
    else:
        return UnknownNode()
