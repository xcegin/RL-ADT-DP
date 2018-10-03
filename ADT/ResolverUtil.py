from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.SequenceNode import SequenceNode
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.BreakStatement import BreakStatement
from ADT.Statements.FunctionCall import FunctionCall
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.ReturnStatement import ReturnStatement
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.UnknowNode import UnknownNode
from ADT.Variables.ArraySubscriptVariable import ArraySubscriptVariable
from ADT.Variables.FieldReferenceVariable import FieldReferenceVariable
from ADT.Variables.OperatorVariable import OperatorVariable
from ADT.Variables.SimpleVariable import SimpleVariable


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
    type = resolveType(type)
    if type == "VariableDeclarationStatement":
        return VariableDeclarationStatement(node["VariableTypeModifiers"], node["VariableType"],
                                            node["Variable"], node["InitialValue"])
    elif type == "IfNode":
        return IfNode(node["Condition"], node["NodeThen"], node["NodeElse"])
    elif type == "LiteralNode":
        return LiteralNode(node["Value"], node["Kind"])
    elif type == "SequenceNode":
        return SequenceNode(node["Nodes"])
    elif type == "AssignmentStatement":
        return AssignmentStatement(node["Variable"], node["Value"])
    elif type == "BreakStatement":
        return BreakStatement()
    elif type == "FunctionCall":
        return FunctionCall(node["Name"], node["Arguments"])
    elif type == "FunctionDeclarationStatement":
        return FunctionDeclarationStatement(node["ReturnTypeModifiers"], node["ReturnType"], node["Name"],
                                            node["Arguments"], node["Body"])
    elif type == "ReturnStatement":
        return ReturnStatement(node["Value"])
    elif type == "VariableDeclarationStatement":
        return VariableDeclarationStatement(node["VariableTypeModifiers"], node["VariableType"], node["Value"],
                                            node["InitialValue"])
    elif type == "ArraySubscriptVariable":
        return ArraySubscriptVariable(node["VariableName"], node["Array"], node["Subscript"])
    elif type == "FieldReferenceVariable":
        return FieldReferenceVariable(node["VariableName"], node["Variable"], node["Dereference"], node["Field"])
    elif type == "OperatorVariable":
        return OperatorVariable(node["VariableName"], node["Operator"])
    elif type == "SimpleVariable":
        return SimpleVariable(node["VariableName"], node["IsReference"], node["isDefinition"], node["isDeclaration"])
    else:
        return UnknownNode()
